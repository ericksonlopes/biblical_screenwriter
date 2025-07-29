"""
Testes para as funções utilitárias do projeto.
"""
import json
import sqlite3
from unittest.mock import patch

from src.models import RoteiroBiblico, DetailVideoYouTube, TipoRoteiro
from src.utils import save_roteiro_json, save_roteiro_sqlite, save_info_video_sqlite


class TestSaveRoteiroJson:
    """Testes para a função save_roteiro_json."""

    def test_save_roteiro_json_criacao_arquivo(self, tmp_path):
        """Testa se o arquivo JSON é criado corretamente."""
        # Mock do OUT_DIR para usar um diretório temporário
        with patch('src.utils.OUT_DIR', tmp_path):
            roteiro = RoteiroBiblico(
                tema="Teste",
                roteiro="Conteúdo do roteiro de teste",
                versiculos_utilizados=["João 3:16"],
                tipo=TipoRoteiro.LONGO
            )

            path = save_roteiro_json(roteiro)

            # Verifica se o arquivo foi criado
            assert path.exists()
            assert path.suffix == ".json"

            # Verifica se o conteúdo está correto
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            assert data["tema"] == "Teste"
            assert data["roteiro"] == "Conteúdo do roteiro de teste"
            assert data["versiculos_utilizados"] == ["João 3:16"]
            assert data["tipo"] == "Video"

    def test_save_roteiro_json_nome_arquivo(self, tmp_path):
        """Testa se o nome do arquivo segue o padrão esperado."""
        with patch('src.utils.OUT_DIR', tmp_path):
            roteiro = RoteiroBiblico(
                tema="Ansiedade e Fé",
                roteiro="Conteúdo",
                versiculos_utilizados=["Filipenses 4:6"],
                tipo=TipoRoteiro.LONGO
            )

            path = save_roteiro_json(roteiro)

            # Verifica se o nome contém timestamp, tipo e tema
            assert "Video" in path.name
            assert "Ansiedade_e_Fé" in path.name
            assert path.name.endswith(".json")


class TestSaveRoteiroSqlite:
    """Testes para a função save_roteiro_sqlite."""

    def test_save_roteiro_sqlite_criacao_banco(self, tmp_path):
        """Testa se o banco SQLite é criado e o roteiro salvo."""
        db_path = tmp_path / "test_roteiros.sqlite3"

        roteiro = RoteiroBiblico(
            tema="Teste SQLite",
            roteiro="Conteúdo do roteiro",
            versiculos_utilizados=["João 3:16", "Romanos 8:28"],
            tipo=TipoRoteiro.LONGO,
            referencias=["Salmo 23"],
            postagem_comunidade="🙏 Acabei de publicar um vídeo sobre ansiedade! Como você lida com momentos de preocupação? Compartilhe suas estratégias nos comentários! ✨"
        )

        roteiro_id = save_roteiro_sqlite(roteiro, str(db_path))

        # Verifica se o banco foi criado
        assert db_path.exists()
        assert roteiro_id == 1  # Primeiro registro

        # Verifica se os dados foram salvos corretamente
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute("SELECT * FROM roteiros_biblicos WHERE id = ?", (roteiro_id,))
        row = cur.fetchone()
        conn.close()

        assert row is not None
        assert row[1] == "Teste SQLite"  # tema
        assert row[3] == "Conteúdo do roteiro"  # roteiro
        assert json.loads(row[4]) == ["João 3:16", "Romanos 8:28"]  # versiculos_utilizados
        assert row[5] == "Video"  # tipo
        assert json.loads(row[6]) == ["Salmo 23"]  # referencias
        assert row[
                   7] == "🙏 Acabei de publicar um vídeo sobre ansiedade! Como você lida com momentos de preocupação? Compartilhe suas estratégias nos comentários! ✨"  # postagem_comunidade

    def test_save_roteiro_sqlite_multiplos_registros(self, tmp_path):
        """Testa se múltiplos roteiros são salvos com IDs incrementais."""
        db_path = tmp_path / "test_roteiros.sqlite3"

        roteiro1 = RoteiroBiblico(
            tema="Primeiro Roteiro",
            roteiro="Conteúdo 1",
            versiculos_utilizados=["João 3:16"],
            tipo=TipoRoteiro.LONGO
        )

        roteiro2 = RoteiroBiblico(
            tema="Segundo Roteiro",
            roteiro="Conteúdo 2",
            versiculos_utilizados=["Romanos 8:28"],
            tipo=TipoRoteiro.SHORT
        )

        id1 = save_roteiro_sqlite(roteiro1, str(db_path))
        id2 = save_roteiro_sqlite(roteiro2, str(db_path))

        assert id1 == 1
        assert id2 == 2


class TestSaveInfoVideoSqlite:
    """Testes para a função save_info_video_sqlite."""

    def test_save_info_video_sqlite_criacao_banco(self, tmp_path):
        """Testa se as informações do vídeo são salvas corretamente."""
        db_path = tmp_path / "test_roteiros.sqlite3"

        # Primeiro cria um roteiro para ter um ID válido
        roteiro = RoteiroBiblico(
            tema="Teste",
            roteiro="Conteúdo",
            versiculos_utilizados=["João 3:16"],
            tipo=TipoRoteiro.LONGO
        )
        roteiro_id = save_roteiro_sqlite(roteiro, str(db_path))

        # Agora salva as informações do vídeo
        info_video = DetailVideoYouTube(
            titulo="Título do Vídeo",
            descricao="Descrição completa do vídeo",
            tags=["tag1", "tag2", "tag3"],
            hashtags=["#hashtag1", "#hashtag2"],
            thumbnail_prompt="Prompt para thumbnail"
        )

        save_info_video_sqlite(info_video, roteiro_id, str(db_path))

        # Verifica se os dados foram salvos
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute("SELECT * FROM info_videos_youtube WHERE roteiro_id = ?", (roteiro_id,))
        row = cur.fetchone()
        conn.close()

        assert row is not None
        assert row[1] == roteiro_id  # roteiro_id
        assert row[2] == "Título do Vídeo"  # titulo
        assert row[3] == "Descrição completa do vídeo"  # descricao
        assert row[4] == "tag1, tag2, tag3"  # tags
        assert row[5] == "#hashtag1, #hashtag2"  # hashtags
        assert row[6] == "Prompt para thumbnail"  # thumbnail_prompt

    def test_save_info_video_sqlite_sem_roteiro_id(self, tmp_path):
        """Testa se a função funciona sem roteiro_id (apenas cria a tabela)."""
        db_path = tmp_path / "test_roteiros.sqlite3"

        info_video = DetailVideoYouTube(
            titulo="Título",
            descricao="Descrição",
            tags=["tag1"],
            hashtags=["#hashtag1"],
            thumbnail_prompt="Prompt"
        )

        # Deve criar a tabela mesmo sem roteiro_id válido
        save_info_video_sqlite(info_video, 999, str(db_path))

        # Verifica se a tabela foi criada
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='info_videos_youtube'")
        table_exists = cur.fetchone() is not None
        conn.close()

        assert table_exists
