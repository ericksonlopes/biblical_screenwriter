# Testes do Projeto Agno Roteirista Bíblico

Este diretório contém os testes automatizados para o projeto Agno Roteirista Bíblico.

## Estrutura dos Testes

```
tests/
├── __init__.py              # Arquivo de inicialização do pacote
├── conftest.py              # Fixtures compartilhadas
├── test_models.py           # Testes dos modelos de dados
├── test_utils.py            # Testes das funções utilitárias
├── test_agents.py           # Testes dos agentes
├── test_integration.py      # Testes de integração
├── test_bible_tool.py       # Testes da ferramenta bíblica
└── README.md                # Esta documentação
```

## Como Executar os Testes

### Executar todos os testes
```bash
pytest tests/
```

### Executar testes específicos
```bash
# Testes de modelos
pytest tests/test_models.py

# Testes de agentes
pytest tests/test_agents.py

# Testes de integração
pytest tests/test_integration.py
```

### Executar com cobertura
```bash
pytest tests/ --cov=src --cov-report=html
```

### Executar com verbose
```bash
pytest tests/ -v
```

## Tipos de Testes

### 1. Testes de Modelos (`test_models.py`)
- Validação de criação de objetos `RoteiroBiblico`
- Validação de criação de objetos `DetailVideoYouTube`
- Testes do enum `TipoRoteiro`
- Validação de campos obrigatórios
- Serialização de modelos

### 2. Testes de Utilitários (`test_utils.py`)
- Salvamento de roteiros em JSON
- Salvamento de roteiros em SQLite
- Salvamento de informações de vídeo
- Criação de bancos de dados
- Tratamento de erros

### 3. Testes de Agentes (`test_agents.py`)
- Geração de roteiros bíblicos
- Geração de informações para YouTube
- Tratamento de erros dos agentes
- Validação de prompts
- Mocks de respostas da API

### 4. Testes de Integração (`test_integration.py`)
- Fluxo completo do sistema
- Simulação do `main.py`
- Validação de dados gerados
- Integração entre componentes

### 5. Testes da Ferramenta Bíblica (`test_bible_tool.py`)
- Busca de versículos
- Tratamento de erros de API
- Validação de referências
- Timeout e erros de rede

## Fixtures Disponíveis

### Fixtures de Dados
- `sample_roteiro`: Roteiro bíblico de exemplo
- `sample_short_roteiro`: Roteiro curto de exemplo
- `sample_detail_video`: Informações de vídeo de exemplo

### Fixtures de Ambiente
- `temp_db_path`: Caminho para banco de dados temporário
- `temp_json_dir`: Diretório temporário para arquivos JSON

## Configuração

### Dependências de Teste
Os testes utilizam as seguintes dependências:
- `pytest`: Framework de testes
- `pytest-cov`: Cobertura de código
- `unittest.mock`: Mocks para testes

### Variáveis de Ambiente
Para executar os testes, certifique-se de que as seguintes variáveis estão configuradas:
- `OPENAI_API_KEY`: Chave da API OpenAI (para testes que não usam mocks)

## Boas Práticas

1. **Isolamento**: Cada teste deve ser independente
2. **Mocks**: Use mocks para dependências externas
3. **Fixtures**: Reutilize dados de teste com fixtures
4. **Nomes Descritivos**: Use nomes claros para testes e funções
5. **Documentação**: Documente testes complexos

## Exemplo de Teste

```python
def test_gerar_roteiro_sucesso(self, mock_agent, sample_roteiro):
    """Testa geração bem-sucedida de roteiro."""
    # Configura mocks
    mock_agent.run.return_value.content = sample_roteiro
    
    # Executa função
    roteiro, roteiro_id = gerar_roteiro("Ansiedade", TipoRoteiro.LONGO)
    
    # Verifica resultado
    assert roteiro.tema == "Ansiedade"
    assert roteiro.tipo == TipoRoteiro.LONGO
    assert roteiro_id > 0
```

## Relatórios

Após executar os testes, você pode gerar relatórios de cobertura:

```bash
# Gerar relatório HTML
pytest tests/ --cov=src --cov-report=html

# Gerar relatório XML (para CI/CD)
pytest tests/ --cov=src --cov-report=xml
```

Os relatórios serão gerados em:
- `htmlcov/`: Relatório HTML de cobertura
- `coverage.xml`: Relatório XML de cobertura 