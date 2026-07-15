# -*- coding: utf-8 -*-
"""
Funções e constantes compartilhadas do projeto
"Fatores Socioeconômicos Associados ao Desempenho no ENEM 2022".

Todos os mapeamentos de códigos foram conferidos no dicionário oficial:
DICIONÁRIO/Dicionário_Microdados_Enem_2022.xlsx (aba MICRODADOS_ENEM_2022).
"""

import sys
from pathlib import Path

import pandas as pd

# Evita erro de encoding ao imprimir acentos no console do Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Caminhos (src/ -> projeto_enem_2022/ -> base enem/)
# ---------------------------------------------------------------------------
PROJETO_DIR = Path(__file__).resolve().parents[1]
BASE_DIR = PROJETO_DIR.parent

CAMINHO_MICRODADOS = BASE_DIR / "DADOS" / "MICRODADOS_ENEM_2022.csv"

PASTA_OUTPUTS = PROJETO_DIR / "outputs"
PASTA_TABELAS = PASTA_OUTPUTS / "tabelas"
PASTA_GRAFICOS = PASTA_OUTPUTS / "graficos"

ARQ_AMOSTRA = PASTA_TABELAS / "amostra_enem_2022.csv"
ARQ_TRATADO = PASTA_TABELAS / "enem_2022_tratado.csv"
ARQ_BASE_PRESENCA = PASTA_TABELAS / "enem_2022_base_presenca.csv"
ARQ_DIAGNOSTICO = PASTA_TABELAS / "diagnostico_tratamento.csv"

# Parâmetros oficiais de leitura dos microdados do INEP
LEITURA_MICRODADOS = dict(sep=";", encoding="latin1")

# ---------------------------------------------------------------------------
# Colunas utilizadas no projeto
# ---------------------------------------------------------------------------
COLUNAS_USAR = [
    "NU_INSCRICAO",
    "NU_ANO",
    "TP_FAIXA_ETARIA",
    "TP_SEXO",
    "TP_COR_RACA",
    "TP_ST_CONCLUSAO",
    "TP_ESCOLA",
    "TP_ENSINO",
    "IN_TREINEIRO",
    "SG_UF_PROVA",
    "NO_MUNICIPIO_PROVA",
    "TP_PRESENCA_CN",
    "TP_PRESENCA_CH",
    "TP_PRESENCA_LC",
    "TP_PRESENCA_MT",
    "NU_NOTA_CN",
    "NU_NOTA_CH",
    "NU_NOTA_LC",
    "NU_NOTA_MT",
    "NU_NOTA_REDACAO",
    "Q001",
    "Q002",
    "Q005",
    "Q006",
    "Q024",
    "Q025",
]

COLUNAS_NOTAS = [
    "NU_NOTA_CN",
    "NU_NOTA_CH",
    "NU_NOTA_LC",
    "NU_NOTA_MT",
    "NU_NOTA_REDACAO",
]

COLUNAS_OBJETIVAS = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT"]

COLUNAS_PRESENCA = [
    "TP_PRESENCA_CN",
    "TP_PRESENCA_CH",
    "TP_PRESENCA_LC",
    "TP_PRESENCA_MT",
]

NOMES_AREAS = {
    "NU_NOTA_CN": "Ciências da Natureza",
    "NU_NOTA_CH": "Ciências Humanas",
    "NU_NOTA_LC": "Linguagens e Códigos",
    "NU_NOTA_MT": "Matemática",
    "NU_NOTA_REDACAO": "Redação",
}

# ---------------------------------------------------------------------------
# Mapeamentos conferidos no dicionário oficial (ENEM 2022)
# ---------------------------------------------------------------------------
MAPA_TP_ESCOLA = {
    1: "Não respondeu",
    2: "Pública",
    3: "Privada",
}

MAPA_COR_RACA = {
    0: "Não declarado",
    1: "Branca",
    2: "Preta",
    3: "Parda",
    4: "Amarela",
    5: "Indígena",
    6: "Não dispõe da informação",
}

MAPA_PRESENCA = {
    0: "Faltou à prova",
    1: "Presente na prova",
    2: "Eliminado na prova",
}

MAPA_TREINEIRO = {
    0: "Não",
    1: "Sim",
}

# Q001 (pai) e Q002 (mãe): "Até que série seu pai/sua mãe estudou?"
MAPA_ESCOLARIDADE = {
    "A": "A - Nunca estudou",
    "B": "B - Fund. I incompleto",
    "C": "C - Fund. I completo",
    "D": "D - Fund. II completo",
    "E": "E - Médio completo",
    "F": "F - Superior completo",
    "G": "G - Pós-graduação",
    "H": "H - Não sabe",
}
ORDEM_ESCOLARIDADE = [MAPA_ESCOLARIDADE[c] for c in "ABCDEFGH"]

# Q006: "Qual é a renda mensal de sua família?" (salário mínimo 2022 = R$ 1.212)
MAPA_RENDA = {
    "A": "A - Nenhuma renda",
    "B": "B - Até R$ 1.212",
    "C": "C - R$ 1.212 a 1.818",
    "D": "D - R$ 1.818 a 2.424",
    "E": "E - R$ 2.424 a 3.030",
    "F": "F - R$ 3.030 a 3.636",
    "G": "G - R$ 3.636 a 4.848",
    "H": "H - R$ 4.848 a 6.060",
    "I": "I - R$ 6.060 a 7.272",
    "J": "J - R$ 7.272 a 8.484",
    "K": "K - R$ 8.484 a 9.696",
    "L": "L - R$ 9.696 a 10.908",
    "M": "M - R$ 10.908 a 12.120",
    "N": "N - R$ 12.120 a 14.544",
    "O": "O - R$ 14.544 a 18.180",
    "P": "P - R$ 18.180 a 24.240",
    "Q": "Q - Acima de R$ 24.240",
}
ORDEM_RENDA = [MAPA_RENDA[c] for c in "ABCDEFGHIJKLMNOPQ"]

# Q024: "Na sua residência tem computador?"
MAPA_COMPUTADOR = {
    "A": "Não possui",
    "B": "Sim, um",
    "C": "Sim, dois",
    "D": "Sim, três",
    "E": "Sim, quatro ou mais",
}
ORDEM_COMPUTADOR = [MAPA_COMPUTADOR[c] for c in "ABCDE"]

# Q025: "Na sua residência tem acesso à Internet?"
MAPA_INTERNET = {
    "A": "Não",
    "B": "Sim",
}


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------
def garantir_pastas():
    """Cria as pastas de saída caso não existam."""
    PASTA_TABELAS.mkdir(parents=True, exist_ok=True)
    PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)


def salvar_csv(df: pd.DataFrame, caminho: Path, index: bool = True) -> None:
    """Salva CSV em UTF-8 com BOM (abre corretamente no Excel)."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=index, encoding="utf-8-sig")
    print(f"  -> salvo: {caminho.relative_to(PROJETO_DIR)}")


def ler_tratado() -> pd.DataFrame:
    """Lê a base tratada (participantes analisáveis)."""
    if not ARQ_TRATADO.exists():
        raise FileNotFoundError(
            f"Base tratada não encontrada em {ARQ_TRATADO}. "
            "Execute antes: 02_criar_amostra.py e 03_tratar_dados.py."
        )
    return pd.read_csv(ARQ_TRATADO, dtype={"NU_INSCRICAO": "string"})


def ler_base_presenca() -> pd.DataFrame:
    """Lê a base de presença (inclui ausentes, exclui treineiros)."""
    if not ARQ_BASE_PRESENCA.exists():
        raise FileNotFoundError(
            f"Base de presença não encontrada em {ARQ_BASE_PRESENCA}. "
            "Execute antes: 02_criar_amostra.py e 03_tratar_dados.py."
        )
    return pd.read_csv(ARQ_BASE_PRESENCA, dtype={"NU_INSCRICAO": "string"})
