# -*- coding: utf-8 -*-
"""
05 - Geração dos gráficos do projeto (matplotlib, PNG em outputs/graficos).

Lê as tabelas geradas por 04_analise_exploratoria.py e a base tratada.
Todos os gráficos usam dpi 300, títulos e eixos nomeados e layout ajustado.
"""

import matplotlib.pyplot as plt
import pandas as pd

from utils import (
    PASTA_GRAFICOS,
    PASTA_TABELAS,
    garantir_pastas,
    ler_tratado,
)

# ---------------------------------------------------------------------------
# Paleta e estilo (paleta categórica validada; superfície clara)
# ---------------------------------------------------------------------------
COR_SERIE_1 = "#2a78d6"   # azul  - série principal
COR_SERIE_2 = "#1baf7a"   # aqua  - série secundária (sempre com rótulo direto)
COR_SUPERFICIE = "#fcfcfb"
COR_TEXTO = "#0b0b0b"
COR_TEXTO_SEC = "#52514e"
COR_MUTED = "#898781"
COR_GRID = "#e1e0d9"
COR_EIXO = "#c3c2b7"

plt.rcParams.update(
    {
        "figure.facecolor": COR_SUPERFICIE,
        "axes.facecolor": COR_SUPERFICIE,
        "savefig.facecolor": COR_SUPERFICIE,
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
        "text.color": COR_TEXTO,
        "axes.labelcolor": COR_TEXTO_SEC,
        "xtick.color": COR_MUTED,
        "ytick.color": COR_MUTED,
        "axes.edgecolor": COR_EIXO,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": COR_GRID,
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 14,
        "figure.dpi": 100,
    }
)

DPI = 300


def ler_tabela(nome: str) -> pd.DataFrame:
    return pd.read_csv(PASTA_TABELAS / nome, index_col=0)


def salvar(fig, nome: str) -> None:
    caminho = PASTA_GRAFICOS / nome
    fig.tight_layout()
    fig.savefig(caminho, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> salvo: {caminho.name}")


def rotular_barras(ax, barras, fmt="{:.0f}", fontsize=9):
    """Rótulo direto no topo de cada barra (para gráficos com poucas categorias)."""
    for barra in barras:
        ax.annotate(
            fmt.format(barra.get_height()),
            (barra.get_x() + barra.get_width() / 2, barra.get_height()),
            ha="center",
            va="bottom",
            fontsize=fontsize,
            color=COR_TEXTO_SEC,
        )


def barras_verticais(tabela, coluna, titulo, xlabel, ylabel, nome_arquivo,
                     rotacao=0, rotular_todas=True):
    n = len(tabela)
    fig, ax = plt.subplots(figsize=(max(8, 0.7 * n + 4), 5.5))
    barras = ax.bar(tabela.index.astype(str), tabela[coluna], color=COR_SERIE_1, width=0.62)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if rotacao:
        plt.setp(ax.get_xticklabels(), rotation=rotacao, ha="right")
    if rotular_todas and n <= 8:
        rotular_barras(ax, barras)
    elif n > 8:
        # rótulos seletivos: apenas o primeiro e o último grupo
        for i in (0, n - 1):
            barra = barras[i]
            ax.annotate(
                f"{barra.get_height():.0f}",
                (barra.get_x() + barra.get_width() / 2, barra.get_height()),
                ha="center", va="bottom", fontsize=9, color=COR_TEXTO_SEC,
            )
    salvar(fig, nome_arquivo)


def main():
    garantir_pastas()
    print("Lendo base tratada e tabelas...")
    df = ler_tratado()

    print("\nGerando gráficos...")

    # ------------------------------------------------------------------
    # 01. Distribuição da média geral
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.hist(df["media_geral"].dropna(), bins=60, color=COR_SERIE_1, edgecolor=COR_SUPERFICIE, linewidth=0.4)
    mediana = df["media_geral"].median()
    ax.axvline(mediana, color=COR_TEXTO_SEC, linewidth=1.2, linestyle="--")
    ax.annotate(f"mediana: {mediana:.0f}", (mediana, ax.get_ylim()[1] * 0.95),
                ha="left", va="top", fontsize=9, color=COR_TEXTO_SEC, xytext=(6, 0),
                textcoords="offset points")
    ax.set_title("Distribuição da média geral - ENEM 2022 (amostra tratada)")
    ax.set_xlabel("Média geral (5 provas)")
    ax.set_ylabel("Número de participantes")
    salvar(fig, "01_distribuicao_media_geral.png")

    # ------------------------------------------------------------------
    # 02. Média por tipo de escola
    # ------------------------------------------------------------------
    escola = ler_tabela("02_media_por_tipo_escola.csv")
    barras_verticais(
        escola, "media_geral",
        "Média geral por tipo de escola - ENEM 2022",
        "Tipo de escola (Ensino Médio)", "Média geral",
        "02_media_por_tipo_escola.png",
    )

    # ------------------------------------------------------------------
    # 03. Média por renda familiar
    # ------------------------------------------------------------------
    renda = ler_tabela("03_media_por_renda.csv")
    barras_verticais(
        renda, "media_geral",
        "Média geral por faixa de renda familiar - ENEM 2022",
        "Faixa de renda familiar (Q006)", "Média geral",
        "03_media_por_renda.png",
        rotacao=45,
    )

    # ------------------------------------------------------------------
    # 04. Média por escolaridade da mãe
    # ------------------------------------------------------------------
    mae = ler_tabela("05_media_por_escolaridade_mae.csv")
    barras_verticais(
        mae, "media_geral",
        "Média geral por escolaridade da mãe - ENEM 2022",
        "Escolaridade da mãe (Q002)", "Média geral",
        "04_media_por_escolaridade_mae.png",
        rotacao=30,
    )

    # ------------------------------------------------------------------
    # 05. Média por cor/raça
    # ------------------------------------------------------------------
    cor = ler_tabela("06_media_por_cor_raca.csv")
    barras_verticais(
        cor, "media_geral",
        "Média geral por cor/raça autodeclarada - ENEM 2022",
        "Cor/raça (autodeclarada)", "Média geral",
        "05_media_por_cor_raca.png",
        rotacao=20,
    )

    # ------------------------------------------------------------------
    # 06. Top 10 UFs por média geral (barras horizontais)
    # ------------------------------------------------------------------
    top10 = ler_tabela("13_top10_ufs_maior_media.csv").sort_values("media_geral")
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.barh(top10.index.astype(str), top10["media_geral"], color=COR_SERIE_1, height=0.62)
    for i, valor in enumerate(top10["media_geral"]):
        ax.annotate(f"{valor:.0f}", (valor, i), ha="left", va="center",
                    fontsize=9, color=COR_TEXTO_SEC, xytext=(4, 0), textcoords="offset points")
    ax.grid(axis="x")
    ax.grid(axis="y", visible=False)
    ax.set_title("10 UFs com maior média geral - ENEM 2022")
    ax.set_xlabel("Média geral")
    ax.set_ylabel("UF de aplicação da prova")
    salvar(fig, "06_top10_ufs_media_geral.png")

    # ------------------------------------------------------------------
    # 07. Internet em casa
    # ------------------------------------------------------------------
    internet = ler_tabela("08_media_por_internet.csv")
    barras_verticais(
        internet, "media_geral",
        "Média geral por acesso à internet em casa - ENEM 2022",
        "Tem acesso à internet em casa? (Q025)", "Média geral",
        "07_media_por_internet.png",
    )

    # ------------------------------------------------------------------
    # 08. Computador em casa
    # ------------------------------------------------------------------
    computador = ler_tabela("09_media_por_computador.csv")
    ordem = ["Não possui", "Sim, um", "Sim, dois", "Sim, três", "Sim, quatro ou mais"]
    computador = computador.reindex([o for o in ordem if o in computador.index])
    barras_verticais(
        computador, "media_geral",
        "Média geral por quantidade de computadores em casa - ENEM 2022",
        "Computador em casa (Q024)", "Média geral",
        "08_media_por_computador.png",
        rotacao=15,
    )

    # ------------------------------------------------------------------
    # 09. Taxa de presença por renda
    # ------------------------------------------------------------------
    presenca = ler_tabela("10_taxa_presenca_por_renda.csv")
    n = len(presenca)
    fig, ax = plt.subplots(figsize=(max(8, 0.7 * n + 4), 5.5))
    barras = ax.bar(presenca.index.astype(str), presenca["taxa_presenca_pct"],
                    color=COR_SERIE_1, width=0.62)
    for i in (0, n - 1):
        barra = barras[i]
        ax.annotate(f"{barra.get_height():.1f}%",
                    (barra.get_x() + barra.get_width() / 2, barra.get_height()),
                    ha="center", va="bottom", fontsize=9, color=COR_TEXTO_SEC)
    ax.set_ylim(0, 100)
    ax.set_title("Taxa de presença em todas as provas por renda familiar - ENEM 2022")
    ax.set_xlabel("Faixa de renda familiar (Q006)")
    ax.set_ylabel("Presentes em todas as provas (%)")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    salvar(fig, "09_taxa_presenca_por_renda.png")

    # ------------------------------------------------------------------
    # 10. Comparativo de notas por área: escola pública x privada
    # ------------------------------------------------------------------
    variacao = ler_tabela("15_variacao_por_area_grupos.csv")
    areas = variacao.index.tolist()
    x = range(len(areas))
    largura = 0.36
    fig, ax = plt.subplots(figsize=(10, 5.5))
    b1 = ax.bar([i - largura / 2 for i in x], variacao["media_escola_publica"],
                width=largura, color=COR_SERIE_1, label="Escola pública")
    b2 = ax.bar([i + largura / 2 for i in x], variacao["media_escola_privada"],
                width=largura, color=COR_SERIE_2, label="Escola privada")
    rotular_barras(ax, b1, fontsize=8)
    rotular_barras(ax, b2, fontsize=8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(areas, rotation=15, ha="right")
    ax.set_title("Média por área da prova: escola pública x privada - ENEM 2022")
    ax.set_xlabel("Área da prova")
    ax.set_ylabel("Média")
    ax.legend(frameon=False, loc="upper left")
    salvar(fig, "10_comparativo_notas_por_area.png")

    print("\nGráficos concluídos.")


if __name__ == "__main__":
    main()
