# 📖 Agno Roteirista Bíblico

Um sistema inteligente para geração automática de roteiros bíblicos otimizados para vídeos do YouTube, utilizando IA para criar conteúdo cristão envolvente e acessível.

## 🎯 Sobre o Projeto

O **Agno Roteirista Bíblico** é uma ferramenta que combina inteligência artificial com ferramentas de busca bíblica para criar roteiros completos para vídeos cristãos. O sistema gera tanto o conteúdo do roteiro quanto as informações otimizadas para SEO do YouTube.

### ✨ Funcionalidades Principais

- **Geração de Roteiros Bíblicos**: Cria roteiros baseados em temas específicos
- **Busca de Versículos**: Integração com Bíblia Online para buscar versículos reais
- **Otimização para YouTube**: Gera títulos, descrições, tags e hashtags otimizadas
- **Dois Formatos**: Suporte para vídeos longos (4-7 min) e shorts (≤60s)
- **Armazenamento**: Salva roteiros em JSON e banco SQLite
- **Thumbnail Prompts**: Gera prompts para criação de thumbnails atrativas

## 🚀 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- Conta OpenAI com API key configurada

### Passos para Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd agno_roteirista_biblico
   ```

2. **Instale as dependências**
   ```bash
   pip install -e .
   ```
   ou usando uv:
   ```bash
   uv sync
   ```

3. **Configure as variáveis de ambiente**
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   OPENAI_API_KEY=sua_chave_api_aqui
   ```

## 📖 Como Usar

### Uso Básico

```python
from src.agents.roteiro_agent import gerar_roteiro
from src.agents.youtube_detail_agent import gerar_detail_video_youtube
from src.models import TipoRoteiro

# Gerar um roteiro longo sobre "Ansiedade"
roteiro, roteiro_id = gerar_roteiro("Ansiedade", TipoRoteiro.LONGO)

# Gerar informações otimizadas para YouTube
info_video = gerar_detail_video_youtube(roteiro, roteiro_id)

print(f"Título: {info_video.titulo}")
print(f"Tags: {info_video.tags}")
```

### Executar o Exemplo Principal

```bash
python main.py
```

## 🏗️ Arquitetura do Projeto

```
agno_roteirista_biblico/
├── main.py                 # Script principal de exemplo
├── pyproject.toml         # Configurações do projeto
├── src/
│   ├── agents/
│   │   ├── roteiro_agent.py      # Agente gerador de roteiros
│   │   └── youtube_info_agent.py # Agente para informações do YouTube
│   ├── bible_tool.py             # Ferramenta de busca bíblica
│   ├── models.py                 # Modelos de dados (Pydantic)
│   └── utils.py                  # Utilitários (JSON/SQLite)
├── roteiros_json/         # Roteiros salvos em JSON
└── roteiros.sqlite3       # Banco de dados SQLite
```

## 🧪 Testes

O projeto inclui uma suíte completa de testes automatizados para garantir a qualidade do código.

### Instalação das Dependências de Teste

```bash
# Usando uv (recomendado)
uv add --dev pytest pytest-cov pytest-mock

# Ou usando pip
pip install pytest pytest-cov pytest-mock
```

### Executando os Testes

```bash
# Executar todos os testes
python -m pytest

# Executar testes específicos
python -m pytest tests/test_models.py
python -m pytest tests/test_utils.py
python -m pytest tests/test_agents.py

# Executar com cobertura
python -m pytest --cov=src --cov-report=html

# Executar com saída detalhada
python -m pytest -v

# Usar o script de conveniência
python run_tests.py --coverage
```

### Estrutura dos Testes

```
tests/
├── conftest.py              # Fixtures compartilhadas
├── test_models.py           # Testes dos modelos de dados
├── test_utils.py            # Testes das funções utilitárias
├── test_agents.py           # Testes dos agentes
├── test_integration.py      # Testes de integração
├── test_bible_tool.py       # Testes da ferramenta bíblica
└── README.md                # Documentação dos testes
```

### Tipos de Testes

- **Testes Unitários**: Testam funções e classes isoladamente
- **Testes de Integração**: Testam a interação entre componentes
- **Testes de Agentes**: Testam os agentes de IA com mocks
- **Testes da Ferramenta Bíblica**: Testam busca e parsing de versículos

Para mais detalhes, consulte [tests/README.md](tests/README.md).

## 🤖 Agentes IA

### Roteiro Agent
- **Modelo**: GPT-4o-mini
- **Função**: Gera roteiros bíblicos baseados em temas
- **Características**:
  - Linguagem acessível e acolhedora
  - Foco na leitura de versículos
  - Evita interpretações complexas
  - Inclui convite para inscrição no canal

### YouTube Info Agent
- **Modelo**: GPT-4o-mini
- **Função**: Otimiza conteúdo para YouTube
- **Saídas**:
  - Títulos chamativos (clickbait positivo)
  - Descrições otimizadas para SEO
  - Tags relevantes para nicho cristão
  - Hashtags populares
  - Prompts para thumbnails

## 📚 Ferramentas

### Bible Lookup Tool
- **Fonte**: Bíblia Online (NTLH)
- **Funcionalidades**:
  - Busca versículos por referência
  - Suporte a intervalos (ex: "rm 5:3-5")
  - Mapeamento de abreviações bíblicas
  - Extração de texto e metadados

**Formato de Referência**:
- `rm 5` - Capítulo completo
- `rm 5:3` - Versículo específico
- `rm 5:3-5` - Intervalo de versículos

## 📊 Modelos de Dados

### RoteiroBiblico
```python
{
    "tema": "Ansiedade",
    "roteiro": "Texto completo do roteiro...",
    "versiculos_utilizados": ["Filipenses 4:6-7", "1 Pedro 5:7"],
    "duracao_estimada": "4-7 minutos",
    "tipo": "Video",  # ou "Short"
    "formato": "Reflexão devocional"
}
```

### DetailVideoYouTube
```python
{
    "titulo": "Título otimizado para SEO",
    "descricao": "Descrição completa do vídeo...",
    "tags": ["cristão", "bíblia", "devocional"],
    "hashtags": ["#cristão", "#bíblia"],
    "thumbnail_prompt": "Prompt para IA gerar thumbnail"
}
```

## 🔧 Configuração

### Variáveis de Ambiente
- `OPENAI_API_KEY`: Chave da API OpenAI (obrigatória)

### Tipos de Roteiro
- `TipoRoteiro.LONGO`: Vídeos de 4-7 minutos (600-900 palavras)
- `TipoRoteiro.SHORT`: Shorts de ≤60 segundos (150-220 palavras)

## 💾 Armazenamento

### JSON
- Localização: `roteiros_json/`
- Formato: Um arquivo por roteiro
- Nomenclatura: `{tema}_{timestamp}.json`

### SQLite
- Arquivo: `roteiros.sqlite3`
- Tabelas: `roteiros`, `info_videos`
- Relacionamento: `roteiro_id` → `info_video`

## 🎨 Exemplo de Saída

### Roteiro Gerado
```
=== ROTEIRO GERADO ===
ID: 1
Tema: Ansiedade
Tipo: Video
Duração: 4-7 minutos

=== INFORMAÇÕES DO VÍDEO ===
Título: 😰 Ansiedade? A Bíblia tem a resposta que você precisa!
Tags: ansiedade, bíblia, paz, cristão, devocional
Hashtags: #ansiedade #paz #bíblia #cristão
Thumbnail Prompt: Uma pessoa em paz, com luz dourada, texto "Ansiedade? A Bíblia responde"
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- **Agno Framework**: Para a infraestrutura de agentes IA
- **Bíblia Online**: Pela API de busca de versículos
- **OpenAI**: Pela tecnologia GPT-4o-mini

## 📞 Suporte

Para dúvidas, sugestões ou problemas:
- Abra uma issue no GitHub
- Entre em contato através do email do projeto

---

**Desenvolvido com ❤️ para a comunidade cristã**
