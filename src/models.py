from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TipoRoteiro(str, Enum):
    LONGO = "Video"
    SHORT = "Short"


class RoteiroBiblico(BaseModel):
    tema: str = Field(..., description="Tema central da reflexão")
    data_criacao: datetime = Field(default_factory=datetime.now, description="Data de criação do roteiro")
    roteiro: str = Field(..., description="Texto integral do roteiro")
    versiculos_utilizados: list[str] = Field(..., description="Referências bíblicas usadas")
    duracao_estimada: str = Field(..., description="Ex.: '3–6 minutos' ou '≤60 segundos'")
    tipo: TipoRoteiro
    referencias: list[str] = Field(default_factory=list, description="Referências sugeridas para o agente usar")
    postagem_comunidade: str = Field(
        default="",
        description="Texto para postagem na comunidade do YouTube, chamando a atenção para o vídeo de forma engajante"
    )


class DetailVideoYouTube(BaseModel):
    titulo: str = Field(..., description="Título chamativo para o vídeo do YouTube")
    descricao: str = Field(..., description="Descrição completa do vídeo para o YouTube")
    tags: list[str] = Field(..., description="Tags relevantes para SEO do YouTube")
    hashtags: list[str] = Field(..., description="Hashtags para redes sociais")
    thumbnail_prompt: str = Field(..., description="Prompt para geração da thumbnail do vídeo")
