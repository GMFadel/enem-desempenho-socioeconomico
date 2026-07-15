# -*- coding: utf-8 -*-
"""
04 - Análise exploratória do ENEM 2022.

Gera tabelas CSV em outputs/tabelas a partir de:
- enem_2022_tratado.csv       (desempenho: sem treineiros, presentes em tudo)
- enem_2022_base_presenca.csv (presença: sem treineiros, inclui ausentes)
"""

import pandas as pd

from utils import (
    COLUNAS_NOTAS,
    NOMES_AREAS,
    ORDEM_ESCOLARIDADE,
    ORDEM_RENDA,
    PASTA_TABELAS,
    garantir_pastas,
    ler_base_presenca,
    ler_tratado,
    salvar_csv,
)

COLUNAS_RESUMO = COLUNAS_NOTAS + ["media_objetivas", "media_geral"]


def media_por_grupo(df: pd.DataFrame, coluna: str, ordem: list[str] | None = None) -> pd.DataFrame:
    """Tabela de médias de notas por grupo, com contagem de participantes."""
    tabela = (
        df.groupby(coluna, dropna=False, observed=True)
        .agg(
            participantes=("NU_INSCRICAO", "count"),
            media_geral=("media_geral", "mean"),
            media_objetivas=("media_objetivas", "mean"),
            media_cn=("NU_NOTA_CN", "mean"),
            media_ch=("NU_NOTA_CH", "mean"),
            media_lc=("NU_NOTA_LC", "mean"),
            media_mt=("NU_NOTA_MT", "mean"),
            media_redacao=("NU_NOTA_REDACAO", "mean"),
        )
        .round(2)
    )
    if ordem is not None:
        tabela = tabela.reindex([g for g in ordem if g in tabela.index])
    else:
        tabela = tabela.sort_values("media_geral", ascending=False)
    return tabela


def taxa_presenca_por_grupo(df: pd.DataFrame, coluna: str, ordem: list[str] | None = None) -> pd.DataFrame:
    """Taxa de presença/ausência por grupo (base sem treineiros, com ausentes)."""
    tabela = (
        df.groupby(coluna, dropna=False, observed=True)
        .agg(
            inscritos=("NU_INSCRICAO", "count"),
            presentes_todas=("presente_todas", "sum"),
        )
    )
    tabela["taxa_presenca_pct"] = (100 * tabela["presentes_todas"] / tabela["inscritos"]).round(2)
    tabela["taxa_ausencia_pct"] = (100 - tabela["taxa_presenca_pct"]).round(2)
    if ordem is not None:
        tabela = tabela.reindex([g for g in ordem if g in tabela.index])
    else:
        tabela = tabela.sort_values("taxa_presenca_pct", ascending=False)
    return tabela


def main():
    garantir_pastas()

    print("Lendo bases tratadas...")
    df = ler_tratado()
    base_presenca = ler_base_presenca()
    print(f"Base de desempenho: {len(df):,} participantes")
    print(f"Base de presença:   {len(base_presenca):,} inscritos (não treineiros)")

    print("\nGerando tabelas...")

    # 1. Resumo geral das notas
    resumo = df[COLUNAS_RESUMO].describe().round(2)
    salvar_csv(resumo, PASTA_TABELAS / "01_resumo_geral_notas.csv")

    # 2-9. Médias por grupo socioeconômico
    salvar_csv(media_por_grupo(df, "tipo_escola"), PASTA_TABELAS / "02_media_por_tipo_escola.csv")
    salvar_csv(media_por_grupo(df, "renda_familiar", ORDEM_RENDA), PASTA_TABELAS / "03_media_por_renda.csv")
    salvar_csv(
        media_por_grupo(df, "escolaridade_pai", ORDEM_ESCOLARIDADE),
        PASTA_TABELAS / "04_media_por_escolaridade_pai.csv",
    )
    salvar_csv(
        media_por_grupo(df, "escolaridade_mae", ORDEM_ESCOLARIDADE),
        PASTA_TABELAS / "05_media_por_escolaridade_mae.csv",
    )
    salvar_csv(media_por_grupo(df, "cor_raca"), PASTA_TABELAS / "06_media_por_cor_raca.csv")
    salvar_csv(media_por_grupo(df, "SG_UF_PROVA"), PASTA_TABELAS / "07_media_por_uf.csv")
    salvar_csv(media_por_grupo(df, "internet_casa"), PASTA_TABELAS / "08_media_por_internet.csv")
    salvar_csv(media_por_grupo(df, "computador_casa"), PASTA_TABELAS / "09_media_por_computador.csv")

    # 10-12. Taxas de presença (base com ausentes)
    salvar_csv(
        taxa_presenca_por_grupo(base_presenca, "renda_familiar", ORDEM_RENDA),
        PASTA_TABELAS / "10_taxa_presenca_por_renda.csv",
    )
    salvar_csv(
        taxa_presenca_por_grupo(base_presenca, "tipo_escola"),
        PASTA_TABELAS / "11_taxa_presenca_por_tipo_escola.csv",
    )
    salvar_csv(
        taxa_presenca_por_grupo(base_presenca, "SG_UF_PROVA"),
        PASTA_TABELAS / "12_taxa_presenca_por_uf.csv",
    )

    # 13-14. Rankings de UF por média geral
    media_uf = media_por_grupo(df, "SG_UF_PROVA")
    salvar_csv(media_uf.head(10), PASTA_TABELAS / "13_top10_ufs_maior_media.csv")
    salvar_csv(media_uf.tail(10).sort_values("media_geral"), PASTA_TABELAS / "14_top10_ufs_menor_media.csv")

    # 15. Variação por área entre grupos socioeconômicos
    # Compara a diferença de média em cada área entre grupos extremos de
    # renda e entre escola pública x privada.
    renda_baixa = df[df["Q006"].isin(["A", "B", "C"])]
    renda_alta = df[df["Q006"].isin(["O", "P", "Q"])]
    publica = df[df["tipo_escola"] == "Pública"]
    privada = df[df["tipo_escola"] == "Privada"]

    linhas = []
    for coluna, nome in NOMES_AREAS.items():
        linhas.append(
            {
                "area": nome,
                "media_renda_baixa_ABC": round(renda_baixa[coluna].mean(), 2),
                "media_renda_alta_OPQ": round(renda_alta[coluna].mean(), 2),
                "diferenca_renda": round(renda_alta[coluna].mean() - renda_baixa[coluna].mean(), 2),
                "media_escola_publica": round(publica[coluna].mean(), 2),
                "media_escola_privada": round(privada[coluna].mean(), 2),
                "diferenca_escola": round(privada[coluna].mean() - publica[coluna].mean(), 2),
            }
        )
    variacao = pd.DataFrame(linhas).set_index("area")
    salvar_csv(variacao, PASTA_TABELAS / "15_variacao_por_area_grupos.csv")

    print("\nAnálise exploratória concluída.")


if __name__ == "__main__":
    main()
