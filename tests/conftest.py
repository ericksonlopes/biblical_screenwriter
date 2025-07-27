"""
Fixtures para os testes do projeto.
"""
import tempfile
from pathlib import Path

import pytest

from src.models import RoteiroBiblico, DetailVideoYouTube, TipoRoteiro


@pytest.fixture
def sample_roteiro():
    """Fixture que retorna um RoteiroBiblico de exemplo."""
    return RoteiroBiblico(
        tema="Ansiedade",
        roteiro="Este é um roteiro de teste sobre ansiedade. Vamos ler Filipenses 4:6-7...",
        versiculos_utilizados=["Filipenses 4:6-7", "Mateus 6:25-34"],
        duracao_estimada="3-6 minutos",
        tipo=TipoRoteiro.LONGO,
        referencias=["Salmo 23", "Isaías 41:10"],
        postagem_comunidade="🙏 Acabei de publicar um vídeo sobre ansiedade! Como você lida com momentos de preocupação? Compartilhe suas estratégias nos comentários! ✨"
    )


@pytest.fixture
def sample_short_roteiro():
    """Fixture que retorna um RoteiroBiblico curto de exemplo."""
    return RoteiroBiblico(
        tema="Gratidão",
        roteiro="Roteiro curto sobre gratidão. 1 Tessalonicenses 5:18...",
        versiculos_utilizados=["1 Tessalonicenses 5:18"],
        duracao_estimada="≤60 segundos",
        tipo=TipoRoteiro.SHORT,
        postagem_comunidade="🙏 Short sobre gratidão! Pelo que você é grato hoje? Deixe nos comentários! ✨"
    )


@pytest.fixture
def sample_detail_video():
    """Fixture que retorna um DetailVideoYouTube de exemplo."""
    return DetailVideoYouTube(
        titulo="Como Vencer a Ansiedade - Reflexão Bíblica",
        descricao="Descrição completa do vídeo sobre ansiedade e fé...",
        tags=["ansiedade", "bíblia", "reflexão", "cristianismo", "fé"],
        hashtags=["#ansiedade", "#bíblia", "#reflexão", "#cristianismo"],
        thumbnail_prompt="Uma pessoa em oração com luz dourada ao fundo"
    )


@pytest.fixture
def temp_db_path():
    """Fixture que retorna um caminho temporário para banco de dados."""
    with tempfile.NamedTemporaryFile(suffix='.sqlite3', delete=False) as f:
        db_path = f.name

    yield db_path

    # Limpeza: remove o arquivo temporário
    try:
        Path(db_path).unlink()
    except FileNotFoundError:
        pass


@pytest.fixture
def temp_json_dir():
    """Fixture que retorna um diretório temporário para arquivos JSON."""
    temp_dir = Path(tempfile.mkdtemp())

    yield temp_dir

    # Limpeza: remove o diretório temporário
    import shutil
    try:
        shutil.rmtree(temp_dir)
    except FileNotFoundError:
        pass
