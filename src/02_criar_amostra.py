# -*- coding: utf-8 -*-
"""
02 - Criação da amostra de trabalho a partir dos microdados completos.

Lê apenas as colunas necessárias (leitura seletiva) e salva a amostra em
outputs/tabelas/amostra_enem_2022.csv.

Uso:
    python 02_criar_amostra.py                  # amostra padrão (300.000 linhas)
    python 02_criar_amostra.py --linhas 500000  # amostra com outro tamanho
    python 02_criar_amostra.py --completa       # base completa, lida em chunks

A leitura em chunks evita estourar a memória ao processar a base completa
(~1,5 GB / mais de 3 milhões de linhas).
"""

import argparse

import pandas as pd

from utils import (
    ARQ_AMOSTRA,
    CAMINHO_MICRODADOS,
    COLUNAS_USAR,
    LEITURA_MICRODADOS,
    garantir_pastas,
    salvar_csv,
)

TAMANHO_PADRAO = 300_000
TAMANHO_CHUNK = 200_000


def colunas_validas() -> list[str]:
    """Confere no cabeçalho quais colunas do projeto existem no arquivo."""
    cabecalho = pd.read_csv(CAMINHO_MICRODADOS, nrows=0, **LEITURA_MICRODADOS)
    disponiveis = set(cabecalho.columns)
    validas = [c for c in COLUNAS_USAR if c in disponiveis]
    ausentes = [c for c in COLUNAS_USAR if c not in disponiveis]
    if ausentes:
        print(f"ATENÇÃO - colunas não encontradas e ignoradas: {ausentes}")
    return validas


def main():
    parser = argparse.ArgumentParser(description="Cria a amostra de trabalho do ENEM 2022.")
    parser.add_argument(
        "--linhas",
        type=int,
        default=TAMANHO_PADRAO,
        help=f"número de linhas da amostra (padrão: {TAMANHO_PADRAO})",
    )
    parser.add_argument(
        "--completa",
        action="store_true",
        help="processa a base completa em chunks, ignorando --linhas",
    )
    args = parser.parse_args()

    garantir_pastas()

    if not CAMINHO_MICRODADOS.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {CAMINHO_MICRODADOS}")

    usecols = colunas_validas()
    # NU_INSCRICAO como texto evita notação científica e perda de dígitos
    dtypes = {"NU_INSCRICAO": "string"}

    if args.completa:
        print("Lendo a BASE COMPLETA em chunks (pode levar alguns minutos)...")
        partes = []
        leitor = pd.read_csv(
            CAMINHO_MICRODADOS,
            usecols=usecols,
            dtype=dtypes,
            chunksize=TAMANHO_CHUNK,
            **LEITURA_MICRODADOS,
        )
        for i, parte in enumerate(leitor, start=1):
            partes.append(parte)
            print(f"  chunk {i:02d}: {len(parte):,} linhas lidas")
        df = pd.concat(partes, ignore_index=True)
    else:
        print(f"Lendo amostra com as primeiras {args.linhas:,} linhas...")
        df = pd.read_csv(
            CAMINHO_MICRODADOS,
            usecols=usecols,
            dtype=dtypes,
            nrows=args.linhas,
            **LEITURA_MICRODADOS,
        )

    print(f"\nLinhas carregadas:  {len(df):,}")
    print(f"Colunas carregadas: {len(df.columns)}")

    salvar_csv(df, ARQ_AMOSTRA, index=False)
    print("\nAmostra criada com sucesso.")


if __name__ == "__main__":
    main()
