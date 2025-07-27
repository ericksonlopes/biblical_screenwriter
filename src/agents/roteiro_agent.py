from datetime import datetime

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from loguru import logger

from src.bible_tool import BibleLookupTool
from src.models import RoteiroBiblico, TipoRoteiro
from src.utils import save_roteiro_json, save_roteiro_sqlite

MODEL_ID = "gpt-4o-mini"

system_prompt = """
Você é um especialista em pesquisa bíblica com profundo conhecimento das escrituras. Sua missão é identificar e juntar versículos bíblicos relevantes que se relacionem com temas específicos para criar conteúdo para vídeos do YouTube.

Diretrizes principais:

1) PESQUISA E SELEÇÃO
- Analise cuidadosamente o tema fornecido
- Identifique versículos que abordem diretamente o tema
- Priorize versículos que se complementem e formem uma narrativa coesa
- Evite versículos fora de contexto ou com interpretações forçadas

2) ORGANIZAÇÃO DO CONTEÚDO
- Agrupe versículos relacionados em blocos temáticos
- Ordene os versículos de forma lógica e fluida
- Mantenha versículos consecutivos unidos quando fizerem parte do mesmo contexto
- Inclua a referência completa de cada versículo (livro, capítulo e versículos)

3) FORMATO DE APRESENTAÇÃO
- Apresente os versículos de forma clara e direta
- Mantenha o foco na leitura dos versículos, sem adicionar interpretações
- Use linguagem respeitosa e reverente
- Para versículos consecutivos, use o formato "Livro X:Y-Z"

4) CONSISTÊNCIA E PRECISÃO
- Verifique a precisão das referências bíblicas
- Mantenha consistência na tradução utilizada
- Certifique-se que os versículos selecionados mantêm seu significado original
- Evite misturar diferentes traduções da Bíblia

5) ASPECTOS TÉCNICOS
- Para vídeos longos: selecione 6-10 blocos de versículos (600-900 palavras)
- Para shorts: selecione 2-3 blocos de versículos (150-220 palavras)
- Mantenha o ritmo adequado para a leitura em vídeo
- Considere pausas naturais entre blocos de versículos

6) CONTEXTUALIZAÇÃO
- Forneça breves indicações de contexto quando estritamente necessário
- Mantenha as transições entre blocos de versículos suaves e naturais
- Evite adicionar comentários ou interpretações pessoais
- Respeite o contexto histórico e literário dos versículos

7) CONCLUSÃO
- Adicione um convite respeitoso para inscrição no canal
- Mantenha o tom pastoral e acolhedor
- Preserve a reverência ao texto sagrado
 
Ao utilizar a ferramenta de busca bíblica:
1. Pesquise primeiro por palavras-chave relacionadas ao tema
2. Verifique o contexto completo dos versículos encontrados
3. Selecione apenas os versículos mais relevantes e apropriados
4. Confirme a precisão das referências antes de incluí-las
"""

bible_tool = BibleLookupTool()

agent = Agent(
    model=OpenAIChat(id=MODEL_ID, temperature=0.3),
    description="Agente gerador de roteiros bíblicos para YouTube",
    tools=[bible_tool],
    response_model=RoteiroBiblico,
    instructions=[system_prompt],
    show_tool_calls=False
)


def gerar_roteiro(titulo: str, tipo: TipoRoteiro = TipoRoteiro, referencias: list[str] = None) -> tuple[RoteiroBiblico, int]:
    """
    Gera um roteiro bíblico baseado no tema e tipo especificados

    Args:
        titulo (str): Tema do roteiro
        tipo (TipoRoteiro): Tipo do roteiro (LONGO ou SHORT)
        referencias (list[str], opcional): Referências sugeridas para o agente usar

    Returns:
        tuple[RoteiroBiblico, int]: Objeto com o roteiro gerado e ID do roteiro no banco
    """
    logger.info(f"Iniciando geração de roteiro: titulo='{titulo}', tipo='{tipo}', referencias={referencias}")
    referencias = referencias or []
    referencias_str = f" Considere utilizar as seguintes referências bíblicas: {', '.join(referencias)}." if referencias else ""
    prompt = (
        f"Gere um roteiro {tipo.value} sobre o tema '{titulo}' seguindo estas diretrizes:\n\n"

        "FORMATO DO ROTEIRO:\n"
        "- Para vídeos longos: 700-1000 palavras (4-7 min)\n"
        "- Para shorts: 150-220 palavras (≤60 s)\n\n"

        "REGRAS ESTRITAS:\n"
        "- Use a ferramenta lookup_verse para buscar versículos relevantes ao tema\n"
        "- Apresente APENAS os versículos bíblicos, sem NENHUM texto adicional\n"
        "- NÃO inclua introduções, explicações, interpretações ou comentários\n"
        "- NÃO adicione transições ou textos conectivos entre os versículos\n"
        "- NÃO inclua reflexões ou conclusões\n\n"

        "FORMATAÇÃO:\n"
        "- Apresente cada versículo no formato 'Livro Capítulo:Versículo(s)'\n"
        "- Para versículos consecutivos, use o formato 'Livro Capítulo:Versículo-Versículo'\n"
        "- Agrupe e leia em sequência contínua todos os versículos consecutivos"
        "- Mantenha versículos consecutivos unidos em um único bloco\n"
        "- Separe blocos diferentes apenas com uma linha em branco\n\n"

        "ESTRUTURA:\n"
        "- Comece cada bloco com a referência bíblica\n"
        "- Apresente o texto do versículo logo após a referência\n"
        "- NÃO adicione nenhum outro elemento além de referência e texto bíblico\n\n"

        "EXEMPLO DE FORMATO:\n"
        "João 3:16\n"
        "[texto do versículo]\n\n"
        "Salmos 23:1-3\n"
        "[texto dos versículos unidos]\n\n"

        f"REFERÊNCIAS SUGERIDAS:\n{referencias_str if referencias_str else '- Use as referências mais adequadas ao tema'}"
    )

    roteiro: RoteiroBiblico = agent.run(prompt).content
    roteiro.referencias = referencias
    roteiro.tema = titulo  # Garantir que o tema seja definido corretamente
    logger.debug(f"Roteiro gerado: {roteiro}")
    path = save_roteiro_json(roteiro)
    roteiro.data_criacao = datetime.now()
    roteiro_id = save_roteiro_sqlite(roteiro)
    logger.success(f"Roteiro salvo em {path} e no banco SQLite com ID {roteiro_id}")
    return roteiro, roteiro_id
