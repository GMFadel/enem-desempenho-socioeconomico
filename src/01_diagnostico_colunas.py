# -*- coding: utf-8 -*-
"""
01 - Diagnóstico de colunas dos Microdados do ENEM 2022.

Confirma que o arquivo MICRODADOS_ENEM_2022.csv existe, lista as colunas
disponíveis e salva a relação em outputs/tabelas/00_colunas_disponiveis.csv.
"""

import pandas as pd

from utils import (
    CAMINHO_MICRODADOS,
    COLUNAS_USAR,
    LEITURA_MICRODADOS,
    PASTA_TABELAS,
    garantir_pastas,
    salvar_csv,
)


def main():
    garantir_pastas()

    print(f"Arquivo esperado: {CAMINHO_MICRODADOS}")
    if not CAMINHO_MICRODADOS.exists():
        raise FileNotFoundError(
            "MICRODADOS_ENEM_2022.csv não encontrado na pasta DADOS. "
            "Baixe os microdados em https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem"
        )
    print("Arquivo encontrado.")

    tamanho_gb = CAMINHO_MICRODADOS.stat().st_size / 1024**3
    print(f"Tamanho do arquivo: {tamanho_gb:.2f} GB")

    print("\nLendo apenas o cabeçalho (nrows=0)...")
    cabecalho = pd.read_csv(CAMINHO_MICRODADOS, nrows=0, **LEITURA_MICRODADOS)
    colunas = list(cabecalho.columns)

    print(f"Total de colunas: {len(colunas)}\n")
    for i, coluna in enumerate(colunas, start=1):
        marca = " (usada no projeto)" if coluna in COLUNAS_USAR else ""
        print(f"{i:02d}. {coluna}{marca}")

    ausentes = [c for c in COLUNAS_USAR if c not in colunas]
    if ausentes:
        print("\nATENÇÃO - colunas esperadas e não encontradas:")
        for c in ausentes:
            print(f"- {c}")
    else:
        print("\nTodas as colunas necessárias ao projeto estão disponíveis.")

    tabela = pd.DataFrame(
        {
            "ordem": range(1, len(colunas) + 1),
            "coluna": colunas,
            "usada_no_projeto": [c in COLUNAS_USAR for c in colunas],
        }
    )
    salvar_csv(tabela, PASTA_TABELAS / "00_colunas_disponiveis.csv", index=False)


if __name__ == "__main__":
    main()
