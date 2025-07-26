#!/usr/bin/env python3
"""
Script para executar os testes do projeto Agno Roteirista Bíblico.
"""
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Executa um comando e exibe o resultado."""
    print(f"\n{'='*50}")
    print(f"Executando: {description}")
    print(f"Comando: {' '.join(cmd)}")
    print(f"{'='*50}\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {e}")
        return False
    except FileNotFoundError:
        print("Erro: pytest não encontrado. Instale com: pip install pytest pytest-cov pytest-mock")
        return False


def main():
    parser = argparse.ArgumentParser(description="Executar testes do projeto")
    parser.add_argument("--unit", action="store_true", help="Executar apenas testes unitários")
    parser.add_argument("--integration", action="store_true", help="Executar apenas testes de integração")
    parser.add_argument("--models", action="store_true", help="Executar testes de modelos")
    parser.add_argument("--utils", action="store_true", help="Executar testes de utilitários")
    parser.add_argument("--agents", action="store_true", help="Executar testes de agentes")
    parser.add_argument("--bible-tool", action="store_true", help="Executar testes da ferramenta bíblica")
    parser.add_argument("--coverage", action="store_true", help="Executar com cobertura de código")
    parser.add_argument("--verbose", "-v", action="store_true", help="Executar com saída detalhada")
    parser.add_argument("--all", action="store_true", help="Executar todos os testes (padrão)")
    
    args = parser.parse_args()
    
    # Verifica se estamos no diretório correto
    if not Path("tests").exists():
        print("Erro: Diretório 'tests' não encontrado. Execute este script na raiz do projeto.")
        sys.exit(1)
    
    # Constrói o comando pytest
    cmd = ["python", "-m", "pytest"]
    
    # Adiciona argumentos baseados nas opções
    if args.verbose:
        cmd.append("-v")
    
    if args.coverage:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term-missing"])
    
    # Define quais testes executar
    if args.unit:
        cmd.extend(["tests/test_models.py", "tests/test_utils.py"])
    elif args.integration:
        cmd.extend(["tests/test_integration.py"])
    elif args.models:
        cmd.extend(["tests/test_models.py"])
    elif args.utils:
        cmd.extend(["tests/test_utils.py"])
    elif args.agents:
        cmd.extend(["tests/test_agents.py"])
    elif args.bible_tool:
        cmd.extend(["tests/test_bible_tool.py"])
    else:
        # Padrão: executa todos os testes
        cmd.append("tests/")
    
    # Executa os testes
    success = run_command(cmd, "Testes do Projeto")
    
    if success:
        print("\n✅ Todos os testes passaram!")
        if args.coverage:
            print("📊 Relatório de cobertura gerado em: htmlcov/index.html")
    else:
        print("\n❌ Alguns testes falharam!")
        sys.exit(1)


if __name__ == "__main__":
    main() 