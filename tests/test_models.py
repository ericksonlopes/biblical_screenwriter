"""
Testes para os modelos de dados do projeto.
"""
import pytest
from datetime import datetime
from src.models import TipoRoteiro, RoteiroBiblico, DetailVideoYouTube


class TestTipoRoteiro:
    """Testes para o enum TipoRoteiro."""
    
    def test_tipo_roteiro_valores(self):
        """Testa se os valores do enum estão corretos."""
        assert TipoRoteiro.LONGO == "Video"
        assert TipoRoteiro.SHORT == "Short"
    
    def test_tipo_roteiro_instancia(self):
        """Testa se é possível criar instâncias do enum."""
        tipo_longo = TipoRoteiro.LONGO
        tipo_short = TipoRoteiro.SHORT
        
        assert isinstance(tipo_longo, TipoRoteiro)
        assert isinstance(tipo_short, TipoRoteiro)


class TestRoteiroBiblico:
    """Testes para o modelo RoteiroBiblico."""
    
    def test_roteiro_biblico_criacao(self):
        """Testa a criação de um RoteiroBiblico válido."""
        roteiro = RoteiroBiblico(
            tema="Ansiedade",
            roteiro="Este é um roteiro de teste sobre ansiedade...",
            versiculos_utilizados=["Filipenses 4:6-7", "Mateus 6:25-34"],
            duracao_estimada="3-6 minutos",
            tipo=TipoRoteiro.LONGO
        )
        
        assert roteiro.tema == "Ansiedade"
        assert roteiro.roteiro == "Este é um roteiro de teste sobre ansiedade..."
        assert len(roteiro.versiculos_utilizados) == 2
        assert roteiro.duracao_estimada == "3-6 minutos"
        assert roteiro.tipo == TipoRoteiro.LONGO
        assert roteiro.formato == "Reflexão devocional"
        assert isinstance(roteiro.data_criacao, datetime)
    
    def test_roteiro_biblico_valores_padrao(self):
        """Testa se os valores padrão são aplicados corretamente."""
        roteiro = RoteiroBiblico(
            tema="Teste",
            roteiro="Roteiro de teste",
            versiculos_utilizados=["João 3:16"],
            duracao_estimada="≤60 segundos",
            tipo=TipoRoteiro.SHORT
        )
        
        assert roteiro.formato == "Reflexão devocional"
        assert roteiro.referencias == []
        assert isinstance(roteiro.data_criacao, datetime)
    
    def test_roteiro_biblico_com_referencias(self):
        """Testa a criação com referências personalizadas."""
        referencias = ["Salmo 23", "Isaías 41:10"]
        roteiro = RoteiroBiblico(
            tema="Conforto",
            roteiro="Roteiro sobre conforto...",
            versiculos_utilizados=["Salmo 23:1-6"],
            duracao_estimada="3-6 minutos",
            tipo=TipoRoteiro.LONGO,
            referencias=referencias
        )
        
        assert roteiro.referencias == referencias
    
    def test_roteiro_biblico_serializacao(self):
        """Testa serialização do modelo."""
        roteiro = RoteiroBiblico(
            tema="Teste",
            roteiro="Roteiro de teste",
            versiculos_utilizados=["João 3:16"],
            duracao_estimada="3-6 minutos",
            tipo=TipoRoteiro.LONGO
        )
        
        # Testa model_dump
        data = roteiro.model_dump()
        assert data["tema"] == "Teste"
        assert data["tipo"] == "Video"
        assert "data_criacao" in data
        
        # Testa model_dump_json
        json_str = roteiro.model_dump_json()
        assert "Teste" in json_str
        assert "Video" in json_str


class TestDetailVideoYouTube:
    """Testes para o modelo DetailVideoYouTube."""
    
    def test_detail_video_youtube_criacao(self):
        """Testa a criação de um DetailVideoYouTube válido."""
        info_video = DetailVideoYouTube(
            titulo="Como Vencer a Ansiedade - Reflexão Bíblica",
            descricao="Descrição completa do vídeo...",
            tags=["ansiedade", "bíblia", "reflexão", "cristianismo"],
            hashtags=["#ansiedade", "#bíblia", "#reflexão"],
            thumbnail_prompt="Uma pessoa em oração com luz dourada"
        )
        
        assert info_video.titulo == "Como Vencer a Ansiedade - Reflexão Bíblica"
        assert info_video.descricao == "Descrição completa do vídeo..."
        assert len(info_video.tags) == 4
        assert len(info_video.hashtags) == 3
        assert info_video.thumbnail_prompt == "Uma pessoa em oração com luz dourada"
    
    def test_detail_video_youtube_listas_vazias(self):
        """Testa se é possível criar com listas vazias."""
        info_video = DetailVideoYouTube(
            titulo="Título",
            descricao="Descrição",
            tags=[],
            hashtags=[],
            thumbnail_prompt="Prompt de teste"
        )
        
        assert info_video.tags == []
        assert info_video.hashtags == []
    
    def test_detail_video_youtube_serializacao(self):
        """Testa serialização do modelo."""
        info_video = DetailVideoYouTube(
            titulo="Título do Vídeo",
            descricao="Descrição completa do vídeo",
            tags=["tag1", "tag2"],
            hashtags=["#hashtag1", "#hashtag2"],
            thumbnail_prompt="Prompt para thumbnail"
        )
        
        # Testa model_dump
        data = info_video.model_dump()
        assert data["titulo"] == "Título do Vídeo"
        assert data["tags"] == ["tag1", "tag2"]
        
        # Testa model_dump_json
        json_str = info_video.model_dump_json()
        assert "Título do Vídeo" in json_str
        assert "tag1" in json_str 