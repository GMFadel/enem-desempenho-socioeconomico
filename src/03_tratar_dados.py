# -*- coding: utf-8 -*-
"""
03 - Tratamento da amostra do ENEM 2022.

A partir de outputs/tabelas/amostra_enem_2022.csv:
- converte as notas para numérico;
- cria presente_todas, media_objetivas e media_geral;
- cria variáveis categóricas legíveis (mapeamentos do dicionário oficial);
- gera duas bases:
    * enem_2022_base_presenca.csv -> sem treineiros, inclui ausentes
      (usada para análise de presença/ausência);
    * enem_2022_tratado.csv       -> sem treineiros e apenas presentes em
      todas as provas (base principal de desempenho);
- salva diagnostico_tratamento.csv com os totais de cada filtro.
"""

import pandas as pd

from utils import (
    ARQ_AMOSTRA,
    ARQ_BASE_PRESENCA,
    ARQ_DIAGNOSTICO,
    ARQ_TRATADO,
    COLUNAS_NOTAS,
    COLUNAS_OBJETIVAS,
    COLUNAS_PRESENCA,
    MAPA_COMPUTADOR,
    MAPA_COR_RACA,
    MAPA_ESCOLARIDADE,
    MAPA_INTERNET,
    MAPA_RENDA,
    MAPA_TP_ESCOLA,
    MAPA_TREINEIRO,
    garantir_pastas,
    salvar_csv,
)


def main():
    garantir_pastas()

    if not ARQ_AMOSTRA.exists():
        raise FileNotFoundError(
            f"Amostra não encontrada em {ARQ_AMOSTRA}. Execute antes: 02_criar_amostra.py."
        )

    print(f"Lendo amostra: {ARQ_AMOSTRA.name}")
    df = pd.read_csv(ARQ_AMOSTRA, dtype={"NU_INSCRICAO": "string"})
    total_amostra = len(df)
    print(f"Linhas da amostra: {total_amostra:,}")

    # ------------------------------------------------------------------
    # Notas para numérico
    # ------------------------------------------------------------------
    for coluna in COLUNAS_NOTAS:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    # ------------------------------------------------------------------
    # Variáveis derivadas
    # ------------------------------------------------------------------
    # presente em todas as provas (código 1 = presente, no dicionário oficial)
    df["presente_todas"] = df[COLUNAS_PRESENCA].eq(1).all(axis=1)

    df["media_objetivas"] = df[COLUNAS_OBJETIVAS].mean(axis=1)
    df["media_geral"] = df[COLUNAS_NOTAS].mean(axis=1)

    # ------------------------------------------------------------------
    # Categóricas legíveis (códigos conferidos no dicionário oficial)
    # ------------------------------------------------------------------
    df["tipo_escola"] = df["TP_ESCOLA"].map(MAPA_TP_ESCOLA)
    df["cor_raca"] = df["TP_COR_RACA"].map(MAPA_COR_RACA)
    df["treineiro"] = df["IN_TREINEIRO"].map(MAPA_TREINEIRO)
    df["escolaridade_pai"] = df["Q001"].map(MAPA_ESCOLARIDADE)
    df["escolaridade_mae"] = df["Q002"].map(MAPA_ESCOLARIDADE)
    df["renda_familiar"] = df["Q006"].map(MAPA_RENDA)
    df["computador_casa"] = df["Q024"].map(MAPA_COMPUTADOR)
    df["internet_casa"] = df["Q025"].map(MAPA_INTERNET)

    # ------------------------------------------------------------------
    # Filtros da análise principal
    # ------------------------------------------------------------------
    total_treineiros = int((df["IN_TREINEIRO"] == 1).sum())
    total_presentes_todas = int(df["presente_todas"].sum())

    # Base de presença: exclui apenas treineiros (mantém ausentes)
    base_presenca = df[df["IN_TREINEIRO"] == 0].copy()

    # Base de desempenho: exclui treineiros e mantém presentes em todas as provas
    base_desempenho = base_presenca[base_presenca["presente_todas"]].copy()
    total_final = len(base_desempenho)

    print(f"\nTreineiros na amostra:            {total_treineiros:,}")
    print(f"Presentes em todas as provas:     {total_presentes_todas:,}")
    print(f"Base analisável (desempenho):     {total_final:,}")
    print(f"Percentual analisável da amostra: {100 * total_final / total_amostra:.1f}%")

    # ------------------------------------------------------------------
    # Salvar bases e diagnóstico
    # ------------------------------------------------------------------
    print("\nSalvando bases tratadas...")
    salvar_csv(base_presenca, ARQ_BASE_PRESENCA, index=False)
    salvar_csv(base_desempenho, ARQ_TRATADO, index=False)

    diagnostico = pd.DataFrame(
        {
            "etapa": [
                "total_amostra_original",
                "total_presentes_todas_as_provas",
                "total_treineiros",
                "total_final_analisavel",
                "percentual_final_analisavel",
            ],
            "valor": [
                total_amostra,
                total_presentes_todas,
                total_treineiros,
                total_final,
                round(100 * total_final / total_amostra, 2),
            ],
        }
    )
    salvar_csv(diagnostico, ARQ_DIAGNOSTICO, index=False)
    print("\nTratamento concluído.")


if __name__ == "__main__":
    main()
