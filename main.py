from dotenv import load_dotenv

from src.agents.roteiro_agent import gerar_roteiro
from src.agents.youtube_detail_agent import gerar_detail_video_youtube
from src.models import TipoRoteiro

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

if __name__ == "__main__":
    # Gerar roteiro bíblico
    roteiro, roteiro_id = gerar_roteiro("fujam da imoralidade sexual", TipoRoteiro.LONGO)

    # Gerar informações do vídeo para YouTube
    info_video = gerar_detail_video_youtube(roteiro, roteiro_id)

    print(f"\n=== ROTEIRO GERADO ===")
    print(f"ID: {roteiro_id}")
    print(f"Tema: {roteiro.tema}")
    print(f"Tipo: {roteiro.tipo}")
    print(f"Duração: {roteiro.duracao_estimada}")

    print(f"\n=== INFORMAÇÕES DO VÍDEO ===")
    print(f"Título: {info_video.titulo}")
    print(f"Tags: {', '.join(info_video.tags)}")
    print(f"Hashtags: {', '.join(info_video.hashtags)}")
    print(f"Thumbnail Prompt: {info_video.thumbnail_prompt}")
    print(f"\nDescrição:\n{info_video.descricao}")
