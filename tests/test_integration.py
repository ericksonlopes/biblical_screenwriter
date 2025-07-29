"""
Testes de integração para o fluxo completo do sistema.
"""
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.agents.roteiro_agent import gerar_roteiro
from src.agents.youtube_detail_agent import gerar_detail_video_youtube
from src.models import RoteiroBiblico, DetailVideoYouTube, TipoRoteiro


class TestFluxoCompleto:
    """Testes para o fluxo completo do sistema."""

    @patch('src.agents.roteiro_agent.agent')
    @patch('src.agents.roteiro_agent.save_roteiro_json')
    @patch('src.agents.roteiro_agent.save_roteiro_sqlite')
    @patch('src.agents.youtube_detail_agent.agent')
    @patch('src.agents.youtube_detail_agent.save_info_video_sqlite')
    def test_fluxo_completo_roteiro_longo(self, mock_save_video, mock_youtube_agent,
                                          mock_save_sqlite, mock_save_json, mock_roteiro_agent):
        """Testa o fluxo completo para um roteiro longo."""
        # Configura mocks do agente de roteiro
        roteiro_response = MagicMock()
        roteiro_response.content = RoteiroBiblico(
            tema="Ansiedade",
            roteiro="Este é um roteiro completo sobre ansiedade. Vamos ler Filipenses 4:6-7...",
            versiculos_utilizados=["Filipenses 4:6-7", "Mateus 6:25-34"],
            tipo=TipoRoteiro.LONGO,
            referencias=["Salmo 23"]
        )
        mock_roteiro_agent.run.return_value = roteiro_response
        mock_save_json.return_value = Path("/tmp/roteiro.json")
        mock_save_sqlite.return_value = 123

        # Configura mocks do agente do YouTube
        video_response = MagicMock()
        video_response.content = DetailVideoYouTube(
            titulo="Como Vencer a Ansiedade - Reflexão Bíblica Completa",
            descricao="Neste vídeo, vamos refletir sobre como a Bíblia nos ensina a lidar com a ansiedade...",
            tags=["ansiedade", "bíblia", "reflexão", "cristianismo", "fé"],
            hashtags=["#ansiedade", "#bíblia", "#reflexão", "#cristianismo"],
            thumbnail_prompt="Uma pessoa em oração com luz dourada ao fundo"
        )
        mock_youtube_agent.run.return_value = video_response

        # Executa o fluxo completo
        roteiro, roteiro_id = gerar_roteiro("Ansiedade", TipoRoteiro.LONGO, ["Salmo 23"])
        info_video = gerar_detail_video_youtube(roteiro, roteiro_id)

        # Verifica o roteiro gerado
        assert roteiro.tema == "Ansiedade"
        assert roteiro.tipo == TipoRoteiro.LONGO
        assert roteiro.referencias == ["Salmo 23"]
        assert len(roteiro.versiculos_utilizados) == 2
        assert roteiro_id == 123

        # Verifica as informações do vídeo
        assert "Ansiedade" in info_video.titulo
        assert "Reflexão Bíblica" in info_video.titulo
        assert len(info_video.tags) >= 4
        assert len(info_video.hashtags) >= 3
        assert "oração" in info_video.thumbnail_prompt.lower()

        # Verifica se todas as funções foram chamadas
        mock_roteiro_agent.run.assert_called_once()
        mock_youtube_agent.run.assert_called_once()
        mock_save_json.assert_called_once()
        mock_save_sqlite.assert_called_once()
        mock_save_video.assert_called_once_with(info_video, 123)

    @patch('src.agents.roteiro_agent.agent')
    @patch('src.agents.roteiro_agent.save_roteiro_json')
    @patch('src.agents.roteiro_agent.save_roteiro_sqlite')
    @patch('src.agents.youtube_detail_agent.agent')
    @patch('src.agents.youtube_detail_agent.save_info_video_sqlite')
    def test_fluxo_completo_roteiro_short(self, mock_save_video, mock_youtube_agent,
                                          mock_save_sqlite, mock_save_json, mock_roteiro_agent):
        """Testa o fluxo completo para um roteiro curto."""
        # Configura mocks do agente de roteiro
        roteiro_response = MagicMock()
        roteiro_response.content = RoteiroBiblico(
            tema="Gratidão",
            roteiro="Roteiro curto sobre gratidão. 1 Tessalonicenses 5:18...",
            versiculos_utilizados=["1 Tessalonicenses 5:18"],
            tipo=TipoRoteiro.SHORT
        )
        mock_roteiro_agent.run.return_value = roteiro_response
        mock_save_json.return_value = Path("/tmp/roteiro_short.json")
        mock_save_sqlite.return_value = 456

        # Configura mocks do agente do YouTube
        video_response = MagicMock()
        video_response.content = DetailVideoYouTube(
            titulo="A Gratidão na Bíblia - Short Inspirador",
            descricao="Reflexão rápida sobre gratidão baseada na Bíblia...",
            tags=["gratidão", "short", "bíblia", "inspiração"],
            hashtags=["#gratidão", "#short", "#inspiração"],
            thumbnail_prompt="Mãos em oração com coração"
        )
        mock_youtube_agent.run.return_value = video_response

        # Executa o fluxo completo
        roteiro, roteiro_id = gerar_roteiro("Gratidão", TipoRoteiro.SHORT)
        info_video = gerar_detail_video_youtube(roteiro, roteiro_id)

        # Verifica o roteiro gerado
        assert roteiro.tema == "Gratidão"
        assert roteiro.tipo == TipoRoteiro.SHORT
        assert roteiro_id == 456

        # Verifica as informações do vídeo
        assert "Gratidão" in info_video.titulo
        assert "Short" in info_video.titulo
        assert "short" in info_video.tags
        assert "#short" in info_video.hashtags

        # Verifica se todas as funções foram chamadas
        mock_roteiro_agent.run.assert_called_once()
        mock_youtube_agent.run.assert_called_once()
        mock_save_json.assert_called_once()
        mock_save_sqlite.assert_called_once()
        mock_save_video.assert_called_once_with(info_video, 456)


class TestIntegracaoComMain:
    """Testes que simulam o fluxo do main.py."""

    @patch('src.agents.roteiro_agent.agent')
    @patch('src.agents.roteiro_agent.save_roteiro_json')
    @patch('src.agents.roteiro_agent.save_roteiro_sqlite')
    @patch('src.agents.youtube_detail_agent.agent')
    @patch('src.agents.youtube_detail_agent.save_info_video_sqlite')
    def test_simulacao_main_py(self, mock_save_video, mock_youtube_agent,
                               mock_save_sqlite, mock_save_json, mock_roteiro_agent):
        """Simula o fluxo executado no main.py."""
        # Configura mocks do agente de roteiro
        roteiro_response = MagicMock()
        roteiro_response.content = RoteiroBiblico(
            tema="Ansiedade",
            roteiro="Este é um roteiro sobre ansiedade. Vamos ler Filipenses 4:6-7...",
            versiculos_utilizados=["Filipenses 4:6-7"],
            tipo=TipoRoteiro.LONGO
        )
        mock_roteiro_agent.run.return_value = roteiro_response
        mock_save_json.return_value = Path("/tmp/roteiro.json")
        mock_save_sqlite.return_value = 789

        # Configura mocks do agente do YouTube
        video_response = MagicMock()
        video_response.content = DetailVideoYouTube(
            titulo="Como Vencer a Ansiedade - Reflexão Bíblica",
            descricao="Descrição completa do vídeo...",
            tags=["ansiedade", "bíblia", "reflexão"],
            hashtags=["#ansiedade", "#bíblia"],
            thumbnail_prompt="Pessoa em oração"
        )
        mock_youtube_agent.run.return_value = video_response

        # Simula o fluxo do main.py
        roteiro, roteiro_id = gerar_roteiro("Ansiedade", TipoRoteiro.LONGO)
        info_video = gerar_detail_video_youtube(roteiro, roteiro_id)

        # Verifica se os dados estão corretos para impressão
        assert roteiro_id == 789
        assert roteiro.tema == "Ansiedade"
        assert roteiro.tipo == TipoRoteiro.LONGO

        assert info_video.titulo == "Como Vencer a Ansiedade - Reflexão Bíblica"
        assert len(info_video.tags) > 0
        assert len(info_video.hashtags) > 0
        assert info_video.thumbnail_prompt == "Pessoa em oração"
        assert len(info_video.descricao) > 0


class TestValidacaoDados:
    """Testes de validação dos dados gerados."""

    @patch('src.agents.roteiro_agent.agent')
    @patch('src.agents.roteiro_agent.save_roteiro_json')
    @patch('src.agents.roteiro_agent.save_roteiro_sqlite')
    @patch('src.agents.youtube_detail_agent.agent')
    @patch('src.agents.youtube_detail_agent.save_info_video_sqlite')
    def test_validacao_dados_roteiro(self, mock_save_video, mock_youtube_agent,
                                     mock_save_sqlite, mock_save_json, mock_roteiro_agent):
        """Testa se os dados do roteiro são válidos."""
        roteiro_response = MagicMock()
        roteiro_response.content = RoteiroBiblico(
            tema="Esperança",
            roteiro="Roteiro sobre esperança...",
            versiculos_utilizados=["Romanos 15:13"],
            tipo=TipoRoteiro.LONGO
        )
        mock_roteiro_agent.run.return_value = roteiro_response
        mock_save_json.return_value = Path("/tmp/roteiro.json")
        mock_save_sqlite.return_value = 101

        video_response = MagicMock()
        video_response.content = DetailVideoYouTube(
            titulo="Título do Vídeo",
            descricao="Descrição do vídeo",
            tags=["tag1"],
            hashtags=["#hashtag1"],
            thumbnail_prompt="Prompt"
        )
        mock_youtube_agent.run.return_value = video_response

        roteiro, roteiro_id = gerar_roteiro("Esperança", TipoRoteiro.LONGO)
        info_video = gerar_detail_video_youtube(roteiro, roteiro_id)

        # Validações do roteiro
        assert isinstance(roteiro.tema, str) and len(roteiro.tema) > 0
        assert isinstance(roteiro.roteiro, str) and len(roteiro.roteiro) > 0
        assert isinstance(roteiro.versiculos_utilizados, list) and len(roteiro.versiculos_utilizados) > 0
        assert roteiro.tipo in [TipoRoteiro.LONGO, TipoRoteiro.SHORT]
        assert isinstance(roteiro_id, int) and roteiro_id > 0

        # Validações das informações do vídeo
        assert isinstance(info_video.titulo, str) and len(info_video.titulo) > 0
        assert isinstance(info_video.descricao, str) and len(info_video.descricao) > 0
        assert isinstance(info_video.tags, list) and len(info_video.tags) > 0
        assert isinstance(info_video.hashtags, list) and len(info_video.hashtags) > 0
        assert isinstance(info_video.thumbnail_prompt, str) and len(info_video.thumbnail_prompt) > 0
