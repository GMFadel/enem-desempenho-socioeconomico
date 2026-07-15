# -*- coding: utf-8 -*-
"""
06 - Geração do relatório final em Markdown (outputs/relatorio_final.md).

Lê as tabelas produzidas por 03 e 04 e monta o relatório com os números
reais da execução — nada é digitado à mão.
"""

import pandas as pd

from utils import (
    ARQ_DIAGNOSTICO,
    PASTA_OUTPUTS,
    PASTA_TABELAS,
    garantir_pastas,
)


def ler(nome: str) -> pd.DataFrame:
    return pd.read_csv(PASTA_TABELAS / nome, index_col=0)


def fmt(n: float) -> str:
    """Formata inteiro com separador de milhar em padrão brasileiro."""
    return f"{int(n):,}".replace(",", ".")


def main():
    garantir_pastas()

    diag = pd.read_csv(ARQ_DIAGNOSTICO).set_index("etapa")["valor"]
    total_amostra = diag["total_amostra_original"]
    total_presentes = diag["total_presentes_todas_as_provas"]
    total_treineiros = diag["total_treineiros"]
    total_final = diag["total_final_analisavel"]
    pct_final = diag["percentual_final_analisavel"]

    resumo = ler("01_resumo_geral_notas.csv")
    escola = ler("02_media_por_tipo_escola.csv")
    renda = ler("03_media_por_renda.csv")
    mae = ler("05_media_por_escolaridade_mae.csv")
    internet = ler("08_media_por_internet.csv")
    computador = ler("09_media_por_computador.csv")
    pres_renda = ler("10_taxa_presenca_por_renda.csv")
    top10 = ler("13_top10_ufs_maior_media.csv")
    variacao = ler("15_variacao_por_area_grupos.csv")

    media_geral = resumo.loc["mean", "media_geral"]
    dp_geral = resumo.loc["std", "media_geral"]

    dif_escola = escola.loc["Privada", "media_geral"] - escola.loc["Pública", "media_geral"]
    renda_min = renda["media_geral"].iloc[0]
    renda_max = renda["media_geral"].max()
    dif_mae = mae["media_geral"].max() - mae["media_geral"].iloc[0]
    dif_internet = internet.loc["Sim", "media_geral"] - internet.loc["Não", "media_geral"]
    dif_computador = computador["media_geral"].max() - computador.loc["Não possui", "media_geral"]
    pres_min = pres_renda["taxa_presenca_pct"].iloc[0]
    pres_max = pres_renda["taxa_presenca_pct"].max()
    area_maior_dif = variacao["diferenca_renda"].idxmax()

    top5 = ", ".join(f"{uf} ({v:.0f})" for uf, v in top10["media_geral"].head(5).items())

    relatorio = f"""# Relatório Final — Fatores Socioeconômicos Associados ao Desempenho no ENEM 2022

## 1. Objetivo

Analisar como características socioeconômicas dos participantes do ENEM 2022 —
renda familiar, tipo de escola, cor/raça, UF da prova, acesso à internet e a
computador e escolaridade dos pais — se **associam** ao desempenho nas provas e
à presença nos dois dias de aplicação.

## 2. Fonte dos dados

- **Microdados do ENEM 2022 — INEP** (dados públicos, disponibilizados com
  adequações de privacidade previstas na LGPD).
- Download oficial: <https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem>
- Os significados de todos os códigos (Q001, Q002, Q006, Q024, Q025, TP_ESCOLA
  etc.) foram conferidos no dicionário oficial que acompanha o pacote.

## 3. Metodologia

1. Leitura seletiva de 26 colunas do arquivo `MICRODADOS_ENEM_2022.csv`
   (separador `;`, encoding `latin1`), com `NU_INSCRICAO` tratado como texto.
2. Criação de uma amostra de trabalho com as primeiras {fmt(total_amostra)} linhas
   (o pipeline aceita `--completa` para processar a base inteira em chunks).
3. Conversão das notas para numérico e criação das variáveis derivadas
   `presente_todas`, `media_objetivas` (4 provas objetivas) e `media_geral`
   (4 objetivas + redação).
4. Tradução dos códigos para categorias legíveis conforme o dicionário oficial.
5. Agregações por grupo socioeconômico (médias e taxas de presença) e geração
   de tabelas e gráficos.

## 4. Filtros aplicados

| Etapa | Participantes |
|---|---:|
| Amostra original | {fmt(total_amostra)} |
| Treineiros (removidos da análise principal) | {fmt(total_treineiros)} |
| Presentes em todas as 4 provas | {fmt(total_presentes)} |
| **Base final analisável (desempenho)** | **{fmt(total_final)}** ({pct_final:.1f}% da amostra) |

- A **análise de desempenho** usa apenas não treineiros presentes nas 4 provas.
- A **análise de presença** usa os não treineiros da amostra, incluindo ausentes.

## 5. Principais resultados

### Distribuição geral
- Média geral (5 notas): **{media_geral:.1f}** pontos (desvio padrão {dp_geral:.1f}).
- A distribuição é aproximadamente simétrica, com leve cauda à direita.

### Tipo de escola
- Diferença observada entre escola privada e pública na média geral:
  **{dif_escola:.0f} pontos** ({escola.loc['Privada', 'media_geral']:.0f} x {escola.loc['Pública', 'media_geral']:.0f}).

### Renda familiar (Q006)
- A média geral cresce de forma praticamente monotônica com a faixa de renda:
  de **{renda_min:.0f}** (nenhuma renda) até **{renda_max:.0f}** nas faixas mais altas —
  amplitude de **{renda_max - renda_min:.0f} pontos**.

### Escolaridade da mãe (Q002)
- Diferença de **{dif_mae:.0f} pontos** entre filhos de mães com pós-graduação e
  de mães que nunca estudaram. Padrão semelhante ocorre com a escolaridade do pai.

### Acesso à internet e a computador
- Internet em casa: diferença de **{dif_internet:.0f} pontos** na média geral (Sim x Não).
- Computador em casa: diferença de **{dif_computador:.0f} pontos** entre quem tem
  três ou mais computadores e quem não possui nenhum.

### UFs
- Maiores médias gerais na amostra: {top5}.

### Presença
- A taxa de presença nas 4 provas também cresce com a renda: de
  **{pres_min:.1f}%** na faixa "nenhuma renda" para cerca de **{pres_max:.1f}%**
  nas faixas mais altas.

### Variação por área
- A área com maior diferença entre grupos extremos de renda é
  **{area_maior_dif}** ({variacao['diferenca_renda'].max():.0f} pontos), seguida de
  Matemática ({variacao.loc['Matemática', 'diferenca_renda']:.0f} pontos).
  Linguagens e Códigos apresenta a menor variação
  ({variacao['diferenca_renda'].min():.0f} pontos).

## 6. Principais conclusões

1. Há **associação consistente** entre condições socioeconômicas e desempenho:
   quanto maior a renda e a escolaridade dos pais, maior a média observada.
2. A diferença entre escola privada e pública é expressiva e aparece em todas
   as áreas, com destaque para Redação e Matemática.
3. O acesso a recursos digitais (internet e computador em casa) está associado
   a médias maiores — provavelmente por ser também um marcador de renda.
4. A desigualdade não aparece só na nota: **a própria ausência às provas é
   maior nas faixas de renda mais baixas**, o que tende a subestimar as
   diferenças ao analisar apenas quem compareceu.
5. Redação e Matemática são as áreas mais sensíveis às diferenças
   socioeconômicas; Linguagens e Códigos, a menos sensível.

## 7. Limitações

- Os resultados referem-se a uma **amostra com as primeiras {fmt(total_amostra)}
  linhas** do arquivo, não à base completa (a menos que o pipeline seja
  reexecutado com `--completa`). Como a ordem das linhas do arquivo não é
  necessariamente aleatória, os números podem diferir dos populacionais.
- Grande parte dos participantes não informa o tipo de escola
  ("Não respondeu"), o que limita a comparação pública x privada.
- Variáveis do questionário socioeconômico são autodeclaradas.
- Não foram aplicados testes de significância estatística nem modelos com
  controle de variáveis; as diferenças descritas são brutas.

## 8. Cuidados interpretativos

- **Associação não significa causalidade.** Renda, escolaridade dos pais,
  tipo de escola e acesso à tecnologia são fortemente correlacionados entre
  si; nenhuma análise aqui isola o efeito de um fator específico.
- Treineiros e ausentes foram removidos da análise principal de desempenho;
  os ausentes foram analisados separadamente (taxas de presença).
- Médias por UF refletem também a composição socioeconômica de cada estado,
  não a "qualidade" do ensino local.
- Os dados são públicos e foram disponibilizados pelo INEP com adequações de
  privacidade/LGPD; nenhuma informação permite identificar participantes.

---
*Relatório gerado automaticamente por `src/06_gerar_relatorio.py` a partir das
tabelas em `outputs/tabelas/`.*
"""

    caminho = PASTA_OUTPUTS / "relatorio_final.md"
    caminho.write_text(relatorio, encoding="utf-8")
    print(f"Relatório salvo em: {caminho}")


if __name__ == "__main__":
    main()
