# Relatório Final — Fatores Socioeconômicos Associados ao Desempenho no ENEM 2022

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
2. Criação de uma amostra de trabalho com as primeiras 300.000 linhas
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
| Amostra original | 300.000 |
| Treineiros (removidos da análise principal) | 21.409 |
| Presentes em todas as 4 provas | 213.049 |
| **Base final analisável (desempenho)** | **195.864** (65.3% da amostra) |

- A **análise de desempenho** usa apenas não treineiros presentes nas 4 provas.
- A **análise de presença** usa os não treineiros da amostra, incluindo ausentes.

## 5. Principais resultados

### Distribuição geral
- Média geral (5 notas): **540.8** pontos (desvio padrão 86.8).
- A distribuição é aproximadamente simétrica, com leve cauda à direita.

### Tipo de escola
- Diferença observada entre escola privada e pública na média geral:
  **95 pontos** (618 x 523).

### Renda familiar (Q006)
- A média geral cresce de forma praticamente monotônica com a faixa de renda:
  de **488** (nenhuma renda) até **666** nas faixas mais altas —
  amplitude de **178 pontos**.

### Escolaridade da mãe (Q002)
- Diferença de **112 pontos** entre filhos de mães com pós-graduação e
  de mães que nunca estudaram. Padrão semelhante ocorre com a escolaridade do pai.

### Acesso à internet e a computador
- Internet em casa: diferença de **50 pontos** na média geral (Sim x Não).
- Computador em casa: diferença de **142 pontos** entre quem tem
  três ou mais computadores e quem não possui nenhum.

### UFs
- Maiores médias gerais na amostra: MG (574), SC (564), SP (564), RS (559), ES (558).

### Presença
- A taxa de presença nas 4 provas também cresce com a renda: de
  **64.4%** na faixa "nenhuma renda" para cerca de **85.6%**
  nas faixas mais altas.

### Variação por área
- A área com maior diferença entre grupos extremos de renda é
  **Redação** (208 pontos), seguida de
  Matemática (190 pontos).
  Linguagens e Códigos apresenta a menor variação
  (102 pontos).

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

- Os resultados referem-se a uma **amostra com as primeiras 300.000
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
