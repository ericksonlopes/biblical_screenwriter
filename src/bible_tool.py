import re
from typing import Dict, Any, List, Optional

import requests
from agno.tools import Toolkit
from loguru import logger
from bs4 import BeautifulSoup

BASE_URL = "https://www.bibliaonline.com.br/{translation}/{slug}/{chapter}"


class BibleLookupTool(Toolkit):
    """
    Busca versículos reais na Bíblia Online (NTLH).
    Aceita referência no formato: 'rm 5', 'rm 5:3', 'rm 5:3-5'.
    Limitação: intervalo deve estar no MESMO capítulo.
    """

    BOOK_ABBREVIATIONS: Dict[str, str] = {
        # — AT —
        "gn": "Gênesis", "ex": "Êxodo", "lv": "Levítico", "nm": "Números",
        "dt": "Deuteronômio", "js": "Josué", "jz": "Juízes", "rt": "Rute",
        "1sm": "1 Samuel", "2sm": "2 Samuel", "1rs": "1 Reis", "2rs": "2 Reis",
        "1cr": "1 Crônicas", "2cr": "2 Crônicas", "ed": "Esdras", "ne": "Neemias",
        "et": "Ester", "jó": "Jó",  # usar 'jó' para diferenciar de João
        "sl": "Salmos", "pv": "Provérbios", "ec": "Eclesiastes", "ct": "Cânticos",
        "is": "Isaías", "jr": "Jeremias", "lm": "Lamentações", "ez": "Ezequiel",
        "dn": "Daniel", "os": "Oséias", "jl": "Joel", "am": "Amós", "ob": "Obadias",
        "jn": "Jonas", "mq": "Miquéias", "na": "Naum", "hc": "Habacuque",
        "sf": "Sofonias", "ag": "Ageu", "zc": "Zacarias", "ml": "Malaquias",
        # — NT —
        "mt": "Mateus", "mc": "Marcos", "lc": "Lucas", "jo": "João",
        "at": "Atos", "rm": "Romanos", "1co": "1 Coríntios", "2co": "2 Coríntios",
        "gl": "Gálatas", "ef": "Efésios", "fp": "Filipenses", "cl": "Colossenses",
        "1ts": "1 Tessalonicenses", "2ts": "2 Tessalonicenses", "1tm": "1 Timóteo",
        "2tm": "2 Timóteo", "tt": "Tito", "fm": "Filemom", "hb": "Hebreus",
        "tg": "Tiago", "1pe": "1 Pedro", "2pe": "2 Pedro", "1jo": "1 João",
        "2jo": "2 João", "3jo": "3 João", "jd": "Judas", "ap": "Apocalipse"
    }

    def __init__(self, **kwargs):
        super().__init__(
            name="bible_lookup_tools",
            tools=[self.lookup_verse],
            **kwargs
        )

    # --------------------------- API pública --------------------------- #
    def lookup_verse(
            self,
            referencia: str,
            translation: str = "ntlh"
    ) -> Dict[str, Any]:
        """
        Retorna texto e metadados de uma referência (capítulo ou versículo).

        Args:
            referencia (str): Referência bíblica no formato 'rm 5', 'rm 5:3', 'rm 5:3-5'.
            translation (str): Tradução da Bíblia (padrão: 'ntlh').
        """
        logger.info(f"Recebida referência: '{referencia}' (tradução: {translation})")
        try:
            livro, cap, v_ini, v_fim = self._parse_ref(referencia)
            logger.debug(f"Referência parseada: livro={livro}, capítulo={cap}, v_ini={v_ini}, v_fim={v_fim}")
        except Exception as e:
            logger.error(f"Erro ao interpretar referência '{referencia}': {e}")
            raise
        url = BASE_URL.format(translation=translation, slug=livro, chapter=cap)
        logger.info(f"GET {url}")

        try:
            raw_html = self._download(url)
        except Exception as e:
            logger.error(f"Erro ao baixar página da bíblia: {e}")
            raise
        try:
            verses = self._extract_verses(raw_html, v_ini, v_fim)
            logger.debug(f"Versículos extraídos: {len(verses)} encontrados")
        except Exception as e:
            logger.error(f"Erro ao extrair versículos: {e}")
            raise
        full_text = " ".join(v["text"] for v in verses)

        ref_fmt = self._format_reference(livro, cap, v_ini, v_fim)
        logger.info(f"Consulta finalizada: {ref_fmt}")
        return {"reference": ref_fmt, "text": full_text, "verses": verses}

    # ------------------------- Métodos privados ------------------------ #
    @classmethod
    def _parse_ref(cls, ref: str) -> tuple[str, str, Optional[int], Optional[int]]:
        """
        Separa slug, capítulo, 1º e 2º versículo (ou None).
        Aceita espaço opcional: 'rm 5:5-7' ou 'rm5:5-7'.
        """
        s = ref.lower().replace(" ", "")
        m = re.fullmatch(r"([1-3]?[a-z]{1,3})([0-9]+)(?::([0-9]+)(?:-([0-9]+))?)?", s)
        if not m:
            logger.warning(f"Formato inválido de referência: '{ref}'")
            raise ValueError("Formato inválido. Ex.: 'rm5', 'rm5:3', 'rm5:3-5'")
        slug, chapter, v1, v2 = m.groups()
        return slug, chapter, int(v1) if v1 else None, int(v2) if v2 else None

    @classmethod
    def _download(cls, url: str) -> str:
        logger.debug(f"Baixando URL: {url}")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        logger.debug(f"Download concluído: {len(resp.text)} caracteres recebidos")
        return resp.text

    @classmethod
    def _extract_verses(
            cls,
            html: str,
            v_start: Optional[int],
            v_end: Optional[int]
    ) -> List[Dict[str, Any]]:
        """
        Coleta pares (nº, texto). Se v_start for None, devolve capítulo inteiro.
        """
        logger.debug(f"Extraindo versículos: v_start={v_start}, v_end={v_end}")
        soup = BeautifulSoup(html, "html.parser")
        spans = soup.find_all("span")

        result, current_num, current_text = [], None, []
        for sp in spans:
            cls = sp.get("class", [])
            # Número do versículo
            if "v" in cls and sp.get_text(strip=True).isdigit():
                if current_num is not None:
                    result.append(
                        {"number": current_num, "text": " ".join(current_text).strip()}
                    )
                current_num = int(sp.get_text(strip=True))
                current_text = []
            # Texto do versículo
            elif "t" in cls:
                current_text.append(sp.get_text(strip=True))

        # adiciona o último verso
        if current_num is not None:
            result.append(
                {"number": current_num, "text": " ".join(current_text).strip()}
            )

        # Filtro por intervalo
        if v_start is None:
            logger.debug(f"Retornando capítulo inteiro: {len(result)} versículos")
            return result
        v_end = v_end or v_start
        if v_end < v_start:
            v_start, v_end = v_end, v_start
        filtrados = [v for v in result if v_start <= v["number"] <= v_end]
        logger.debug(f"Versículos filtrados: {len(filtrados)} retornados")
        return filtrados

    def _format_reference(
            self,
            slug: str,
            cap: str,
            v_start: Optional[int],
            v_end: Optional[int]
    ) -> str:
        livro = self.BOOK_ABBREVIATIONS.get(slug, slug.upper())
        if v_start is None:
            return f"{livro} {cap} (NTLH)"
        if v_end and v_end != v_start:
            return f"{livro} {cap}:{v_start}-{v_end} (NTLH)"
        return f"{livro} {cap}:{v_start} (NTLH)"
