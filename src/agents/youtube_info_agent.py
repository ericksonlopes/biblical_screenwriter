from agno.agent import Agent
from agno.models.openai import OpenAIChat
from loguru import logger

from src.models import InfoVideoYouTube, RoteiroBiblico
from src.utils import save_info_video_sqlite

MODEL_ID = "gpt-4o-mini"

system_prompt = """
Você é um especialista em marketing digital e SEO para YouTube, focado em conteúdo cristão e bíblico. 
Sua missão é criar informações otimizadas para vídeos do YouTube baseadas em roteiros bíblicos.

Siga estas diretrizes:
1) Crie títulos chamativos e que gerem cliques (clickbait positivo)
2) Use palavras-chave relevantes para SEO cristão
3) Inclua emojis apropriados para engajamento
4) Mantenha o foco no conteúdo bíblico e espiritual
5) Otimize para o algoritmo do YouTube
6) Use hashtags populares no nicho cristão
7) Crie descrições que incentivem inscrições e engajamento
"""

agent = Agent(
    model=OpenAIChat(id=MODEL_ID, temperature=0.7),
    description="Agente gerador de informações para vídeos do YouTube",
    response_model=InfoVideoYouTube,
    instructions=[system_prompt],
    show_tool_calls=False
)


def gerar_info_video_youtube(roteiro: RoteiroBiblico, roteiro_id: int = None) -> InfoVideoYouTube:
    """
    Gera informações otimizadas para vídeo do YouTube baseadas no roteiro bíblico.

    Args:
        roteiro (RoteiroBiblico): Roteiro bíblico para gerar as informações
        roteiro_id (int, opcional): ID do roteiro no banco de dados

    Returns:
        InfoVideoYouTube: Objeto com as informações do vídeo
    """
    logger.info(f"Gerando informações do vídeo para roteiro: tema='{roteiro.tema}', tipo='{roteiro.tipo}'")
    
    prompt = f"""
    Com base no seguinte roteiro bíblico, crie informações otimizadas para um vídeo do YouTube:

    TEMA: {roteiro.tema}
    TIPO: {roteiro.tipo.value}
    DURAÇÃO: {roteiro.duracao_estimada}
    VERSÍCULOS: {', '.join(roteiro.versiculos_utilizados)}
    
    ROTEIRO:
    {roteiro.roteiro}

    Crie:
    1) Um título chamativo e otimizado para SEO que chame a atenção do público
    2) Uma descrição completa que incentive inscrições
    3) Tags relevantes para o nicho cristão
    4) Hashtags populares para redes sociais
    5) Um prompt para gerar uma thumbnail atrativa

    Foque em engajamento e conversão para inscritos no canal.
    """

    info_video: InfoVideoYouTube = agent.run(prompt).content
    logger.debug(f"Informações do vídeo geradas: {info_video}")
    
    if roteiro_id:
        save_info_video_sqlite(info_video, roteiro_id)
        logger.success(f"Informações do vídeo salvas no banco SQLite")
    
    return info_video 