import json
import sqlite3
from datetime import datetime
from pathlib import Path

from loguru import logger

from src.models import RoteiroBiblico, DetailVideoYouTube

OUT_DIR = Path(__file__).resolve().parent.parent / "roteiros_json"
OUT_DIR.mkdir(exist_ok=True)


def save_roteiro_json(roteiro: RoteiroBiblico) -> Path:
    logger.info(f"Salvando roteiro: tema='{roteiro.tema}', tipo='{roteiro.tipo}'")
    ts = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    f_name = f"{ts}_{roteiro.tipo}_{roteiro.tema.replace(' ', '_')}.json"
    path = OUT_DIR / f_name
    with path.open("w", encoding="utf-8") as f:
        json.dump(roteiro.model_dump(mode="json"), f, ensure_ascii=False, indent=2)
    logger.success(f"Roteiro salvo em {path}")
    return path


def save_roteiro_sqlite(roteiro: RoteiroBiblico, db_path: str = None) -> int:
    """
    Salva o roteiro em um banco SQLite. Se o banco não existir, cria a tabela.
    Listas são armazenadas como JSON.
    
    Returns:
        int: ID do roteiro inserido
    """
    if db_path is None:
        db_path = str((Path(__file__).resolve().parent.parent / "roteiros.sqlite3"))
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS roteiros_biblicos
                (
                    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
                    tema                  TEXT,
                    data_criacao          TEXT,
                    roteiro               TEXT,
                    versiculos_utilizados TEXT,
                    duracao_estimada      TEXT,
                    tipo                  TEXT,
                    referencias           TEXT
                )
                ''')
    cur.execute('''
                INSERT INTO roteiros_biblicos (tema, data_criacao, roteiro, versiculos_utilizados, duracao_estimada,
                                               tipo, referencias)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    roteiro.tema,
                    roteiro.data_criacao.isoformat(),
                    roteiro.roteiro,
                    json.dumps(roteiro.versiculos_utilizados, ensure_ascii=False),
                    roteiro.duracao_estimada,
                    roteiro.tipo.value if hasattr(roteiro.tipo, 'value') else str(roteiro.tipo),
                    json.dumps(roteiro.referencias, ensure_ascii=False)
                ))
    roteiro_id = cur.lastrowid
    conn.commit()
    conn.close()
    logger.success(f"Roteiro salvo no banco SQLite em {db_path} com ID {roteiro_id}")
    return roteiro_id


def save_info_video_sqlite(info_video: DetailVideoYouTube, roteiro_id: int, db_path: str = None) -> None:
    """
    Salva as informações do vídeo do YouTube em um banco SQLite.
    """
    if db_path is None:
        db_path = str((Path(__file__).resolve().parent.parent / "roteiros.sqlite3"))
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS info_videos_youtube
                (
                    id               INTEGER PRIMARY KEY AUTOINCREMENT,
                    roteiro_id       INTEGER,
                    titulo           TEXT,
                    descricao        TEXT,
                    tags             TEXT,
                    hashtags         TEXT,
                    thumbnail_prompt TEXT,
                    FOREIGN KEY (roteiro_id) REFERENCES roteiros_biblicos (id)
                )
                ''')
    cur.execute('''
                INSERT INTO info_videos_youtube (roteiro_id, titulo, descricao, tags, hashtags, thumbnail_prompt)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    roteiro_id,
                    info_video.titulo,
                    info_video.descricao,
                    ", ".join(info_video.tags),
                    ", ".join(info_video.hashtags),
                    info_video.thumbnail_prompt
                ))
    conn.commit()
    conn.close()
    logger.success(f"Informações do vídeo salvas no banco SQLite para roteiro_id {roteiro_id}")
