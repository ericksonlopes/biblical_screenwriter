"""
Testes para a ferramenta de busca bíblica.
"""
import pytest
from unittest.mock import patch, MagicMock
import requests

from src.bible_tool import BibleLookupTool


class TestBibleLookupTool:
    """Testes para a ferramenta BibleLookupTool."""
    
    def test_bible_lookup_tool_instancia(self):
        """Testa se a ferramenta pode ser instanciada."""
        tool = BibleLookupTool()
        assert tool is not None
        assert hasattr(tool, 'lookup_verse')
    
    @patch('requests.get')
    def test_lookup_verse_sucesso(self, mock_get):
        """Testa busca bem-sucedida de versículo."""
        # Configura mock da resposta da API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''<span class="v">16</span><span class="t">Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito...</span>'''
        mock_get.return_value = mock_response
        
        tool = BibleLookupTool()
        result = tool.lookup_verse("jo3:16")

        # Verifica se a requisição foi feita corretamente
        mock_get.assert_called_once()
        assert result["reference"].startswith("João 3:16")
        assert "Deus amou o mundo" in result["text"]
        assert len(result["verses"]) == 1
        assert result["verses"][0]["number"] == 16

    @patch('requests.get')
    def test_lookup_verse_erro_api(self, mock_get):
        """Testa tratamento de erro da API."""
        # Configura mock para simular erro da API
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Versículo não encontrado"
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

        tool = BibleLookupTool()
        result = tool.lookup_verse("jo3:99")
        assert "error" in result
        assert "erro" in result["error"].lower() or "não encontrado" in result["error"].lower()

    @patch('requests.get')
    def test_lookup_verse_erro_rede(self, mock_get):
        """Testa tratamento de erro de rede."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Falha de conexão")
        tool = BibleLookupTool()
        result = tool.lookup_verse("rm5:3")
        assert "error" in result
        assert "erro" in result["error"].lower()

    def test_lookup_verse_formato_referencia(self):
        """Testa tratamento de formato inválido de referência."""
        tool = BibleLookupTool()
        result = tool.lookup_verse("formato_invalido")
        assert "error" in result
        assert "formato inválido" in result["error"].lower()

    def test_lookup_verse_caracteres_especiais(self):
        """Testa tratamento de referência com caracteres especiais."""
        tool = BibleLookupTool()
        result = tool.lookup_verse("rm$5:3")
        assert "error" in result
        assert "formato inválido" in result["error"].lower()

    @patch('requests.get')
    def test_lookup_verse_parametros_invalidos(self, mock_get):
        """Testa tratamento de parâmetros inválidos."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = ""
        mock_get.return_value = mock_response
        tool = BibleLookupTool()
        result = tool.lookup_verse("rm5:999")
        assert "error" in result
        assert "não encontrado" in result["error"].lower()

    @patch('requests.get')
    def test_lookup_verse_timeout(self, mock_get):
        """Testa tratamento de timeout."""
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")
        tool = BibleLookupTool()
        result = tool.lookup_verse("rm5:3")
        assert "error" in result
        assert "erro" in result["error"].lower()

    @patch('requests.get')
    def test_lookup_verse_resposta_invalida(self, mock_get):
        """Testa tratamento de resposta inválida da API."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Sem versículos</body></html>"
        mock_get.return_value = mock_response
        tool = BibleLookupTool()
        result = tool.lookup_verse("rm5:3")
        assert "error" in result
        assert "erro" in result["error"].lower() or "não encontrado" in result["error"].lower()
