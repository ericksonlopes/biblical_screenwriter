"""
Testes para os agentes do projeto.
"""
from unittest.mock import patch

import pytest

from src.agents.roteiro_agent import gerar_roteiro
from src.agents.youtube_detail_agent import gerar_detail_video_youtube
from src.models import TipoRoteiro


class TestRoteiroAgent:
    """Testes para o agente de geração de roteiros."""

    @patch('src.agents.roteiro_agent.agent')
    @patch('src.agents.roteiro_agent.save_roteiro_json')
    @patch('src.agents.roteiro_agent.save_roteiro_sqlite')
    def test_gerar_roteiro_sucesso(self, mock_save_sqlite, mock_save_json, mock_agent, sample_roteiro):
        """Testa geração bem-sucedida de roteiro."""
        # Configura os mocks
        mock_agent.run.return_value.content = sample_roteiro
        mock_save_json.return_value = "caminho/para/arquivo.json"
        mock_save_sqlite.return_value = 123

        # Executa a função
        roteiro, roteiro_id = gerar_roteiro("Ansiedade", TipoRoteiro.LONGO)

        # Verifica se o agente foi chamado
        mock_agent.run.assert_called_once()
        call_args = mock_agent.run.call_args[0][0]
        assert "Ansiedade" in call_args
        assert "Video" in call_args  # TipoRoteiro.LONGO.value

        # Verifica se as funções de salvamento foram chamadas
        mock_save_json.assert_called_once_with(sample_roteiro)
        mock_save_sqlite.assert_called_once_with(sample_roteiro)

        # Verifica o retorno
        assert roteiro == sample_roteiro
        assert roteiro_id == 123

    @patch('src.agents.roteiro_agent.agent')
    @patch('src.agents.roteiro_agent.save_roteiro_json')
    @patch('src.agents.roteiro_agent.save_roteiro_sqlite')
    def test_gerar_roteiro_com_referencias(self, mock_save_sqlite, mock_save_json, mock_agent, sample_roteiro):
        """Testa geração de roteiro com referências personalizadas."""
        mock_agent.run.return_value.content = sample_roteiro
        mock_save_json.return_value = "caminho/para/arquivo.json"
        mock_save_sqlite.return_value = 456

        referencias = ["Salmo 23", "Isaías 41:10"]
        roteiro, roteiro_id = gerar_roteiro("Conforto", TipoRoteiro.LONGO, referencias)

        # Verifica se as referências foram incluídas no prompt
        call_args = mock_agent.run.call_args[0][0]
        assert "Salmo 23" in call_args
        assert "Isaías 41:10" in call_args

        # Verifica se as referências foram salvas no roteiro
        assert roteiro.referencias == referencias

    @patch('src.agents.roteiro_agent.agent')
    @patch('src.agents.roteiro_agent.save_roteiro_json')
    @patch('src.agents.roteiro_agent.save_roteiro_sqlite')
    def test_gerar_roteiro_short(self, mock_save_sqlite, mock_save_json, mock_agent, sample_short_roteiro):
        """Testa geração de roteiro curto."""
        mock_agent.run.return_value.content = sample_short_roteiro
        mock_save_json.return_value = "caminho/para/arquivo.json"
        mock_save_sqlite.return_value = 789

        roteiro, roteiro_id = gerar_roteiro("Gratidão", TipoRoteiro.SHORT)

        # Verifica se o prompt inclui instruções para shorts
        call_args = mock_agent.run.call_args[0][0]
        assert "Short" in call_args

        assert roteiro.tipo == TipoRoteiro.SHORT
        assert roteiro_id == 789

    @patch('src.agents.roteiro_agent.agent')
    def test_gerar_roteiro_erro_agente(self, mock_agent):
        """Testa tratamento de erro quando o agente falha."""
        mock_agent.run.side_effect = Exception("Erro no agente")

        with pytest.raises(Exception, match="Erro no agente"):
            gerar_roteiro("Teste", TipoRoteiro.LONGO)


class TestYouTubeDetailAgent:
    """Testes para o agente de geração de informações do YouTube."""

    @patch('src.agents.youtube_detail_agent.agent')
    @patch('src.agents.youtube_detail_agent.save_info_video_sqlite')
    def test_gerar_detail_video_youtube_sucesso(self, mock_save_sqlite, mock_agent, sample_detail_video,
                                                sample_roteiro):
        """Testa geração bem-sucedida de informações do vídeo."""
        mock_agent.run.return_value.content = sample_detail_video

        info_video = gerar_detail_video_youtube(sample_roteiro, 123)

        # Verifica se o agente foi chamado
        mock_agent.run.assert_called_once()
        call_args = mock_agent.run.call_args[0][0]
        assert sample_roteiro.tema in call_args
        assert sample_roteiro.tipo.value in call_args

        # Verifica se a função de salvamento foi chamada
        mock_save_sqlite.assert_called_once_with(sample_detail_video, 123)

        # Verifica o retorno
        assert info_video == sample_detail_video

    @patch('src.agents.youtube_detail_agent.agent')
    @patch('src.agents.youtube_detail_agent.save_info_video_sqlite')
    def test_gerar_detail_video_youtube_sem_roteiro_id(self, mock_save_sqlite, mock_agent, sample_detail_video,
                                                       sample_roteiro):
        """Testa geração sem roteiro_id (não salva no banco)."""
        mock_agent.run.return_value.content = sample_detail_video

        info_video = gerar_detail_video_youtube(sample_roteiro)

        # Verifica se o agente foi chamado
        mock_agent.run.assert_called_once()

        # Verifica que a função de salvamento NÃO foi chamada
        mock_save_sqlite.assert_not_called()

        # Verifica o retorno
        assert info_video == sample_detail_video

    @patch('src.agents.youtube_detail_agent.agent')
    def test_gerar_detail_video_youtube_erro_agente(self, mock_agent, sample_roteiro):
        """Testa tratamento de erro quando o agente falha."""
        mock_agent.run.side_effect = Exception("Erro no agente do YouTube")

        with pytest.raises(Exception, match="Erro no agente do YouTube"):
            gerar_detail_video_youtube(sample_roteiro)

    @patch('src.agents.youtube_detail_agent.agent')
    @patch('src.agents.youtube_detail_agent.save_info_video_sqlite')
    def test_gerar_detail_video_youtube_prompt_completo(self, mock_save_sqlite, mock_agent, sample_detail_video,
                                                        sample_roteiro):
        """Testa se o prompt inclui todas as informações necessárias."""
        mock_agent.run.return_value.content = sample_detail_video

        gerar_detail_video_youtube(sample_roteiro, 456)

        call_args = mock_agent.run.call_args[0][0]

        # Verifica se todas as informações do roteiro estão no prompt
        assert sample_roteiro.tema in call_args
        assert sample_roteiro.tipo.value in call_args
        assert sample_roteiro.roteiro in call_args

        # Verifica se os versículos estão no prompt
        for versiculo in sample_roteiro.versiculos_utilizados:
            assert versiculo in call_args
