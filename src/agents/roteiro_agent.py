from datetime import datetime

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from loguru import logger

from src.bible_tool import BibleLookupTool
from src.models import RoteiroBiblico, TipoRoteiro
from src.utils import save_roteiro_json, save_roteiro_sqlite

MODEL_ID = "gpt-4o-mini"

system_prompt = """
Você é um redator cristão acolhedor com foco em leitura biblica. Sua missão é criar roteiros bíblicos para vídeos do YouTube que foquem na leitura de versículos.

Siga estas diretrizes:
1) Seja direto e claro, evitando rodeios
2) Comece com uma pergunta instigante
3) Convide o público a ouvir os proximos versículos até o final
4) Foque na leitura de versículos bíblicos, evitando interpretações complexas
5) Evite jargões teológicos complexos; use linguagem acessível.
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


def gerar_roteiro(titulo: str, tipo: TipoRoteiro = TipoRoteiro, referencias: list[str] = None) -> tuple[
    RoteiroBiblico, int]:
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
        f"Gere um roteiro {tipo.value} sobre o tema '{titulo}'. "
        "Para vídeos longos, use 600–900 palavras (4–7 min). "
        "Para shorts, use 150–220 palavras (≤60 s). "
        "Use a ferramenta lookup_verse para buscar os versículos pertinente antes de escrever o roteiro."
        "Não inclua explicações ou interpretações entre os versículos, apenas leia-os. "
        "Se o próximo versículo for a continuação do anterior, leia-os juntos, como parte do mesmo contexto, sem dividir a fala. "
        "Agrupe e leia em sequência contínua todos os versículos consecutivos, formando blocos únicos (exemplo: 'Livro 1:1-7 diz: ...'). "
        "Não faça pausas ou divisões desnecessárias entre versículos que pertencem ao mesmo bloco contínuo. "
        "Mostre claramente quais versículos estão sendo lidos, citando o intervalo corretamente. "
        "Conclua o roteiro com uma reflexão final que resuma a mensagem central do tema. "
        "Ao finalizar, inclua um convite a se inscrever no canal e ativar o sininho para receber notificações de novos vídeos. "
        f"Referencia: {referencias_str}"
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
