# Metodologia

## 1. Dados

- **Fonte:** Microdados do ENEM 2022, publicados pelo INEP
  (<https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem>).
- Arquivo principal: `DADOS/MICRODADOS_ENEM_2022.csv` (~1,5 GB, 76 colunas,
  separador `;`, encoding `latin1`).
- Os dados são públicos e foram disponibilizados pelo INEP já com adequações
  de privacidade previstas na LGPD (sem nomes ou dados identificáveis).

## 2. Leitura e amostragem

- **Leitura seletiva**: apenas as 26 colunas relevantes são carregadas
  (`usecols`), o que reduz drasticamente o uso de memória.
- `NU_INSCRICAO` é lido como **texto** para evitar notação científica e perda
  de dígitos.
- **Amostra de trabalho**: por padrão, as primeiras **300.000 linhas** do
  arquivo (`02_criar_amostra.py`). O tamanho é configurável (`--linhas N`) e
  há a opção `--completa`, que processa a base inteira em **chunks** de
  200.000 linhas para não estourar a memória.

## 3. Tratamento (`03_tratar_dados.py`)

1. Notas convertidas para numérico (`errors="coerce"`).
2. `presente_todas`: participante com `TP_PRESENCA == 1` nas 4 provas objetivas.
3. `media_objetivas`: média de CN, CH, LC e MT.
4. `media_geral`: média das 4 objetivas + Redação.
5. Códigos traduzidos para categorias legíveis **conferidas no dicionário
   oficial** (ver `data_dictionary.md`).
6. Duas bases de saída:
   - **Base de desempenho** (`enem_2022_tratado.csv`): exclui treineiros
     (`IN_TREINEIRO == 1`) e mantém apenas presentes nas 4 provas.
   - **Base de presença** (`enem_2022_base_presenca.csv`): exclui apenas
     treineiros e mantém os ausentes — usada para as taxas de presença.
7. Diagnóstico dos filtros salvo em `diagnostico_tratamento.csv`.

### Por que remover treineiros e ausentes da análise de desempenho?

- **Treineiros** fazem a prova sem valer para ingresso; seu comportamento
  (motivação, preparo) difere do participante regular.
- **Ausentes** não possuem notas em todas as provas; mantê-los distorceria
  médias e comparações. A ausência é analisada **separadamente**, como
  fenômeno de interesse próprio (varia por renda, escola e UF).

## 4. Análise (`04_analise_exploratoria.py`)

- Médias de cada nota e da média geral por grupo: tipo de escola, renda
  familiar, escolaridade do pai e da mãe, cor/raça, UF, internet e computador
  em casa — sempre com a contagem de participantes por grupo.
- Taxas de presença (percentual de inscritos presentes nas 4 provas) por
  renda, tipo de escola e UF, calculadas na base **com** ausentes.
- Rankings de UF (10 maiores e 10 menores médias).
- Variação por área da prova entre grupos extremos de renda (faixas A–C vs
  O–Q) e entre escola pública e privada.

## 5. Visualização (`05_gerar_graficos.py`)

- matplotlib puro (sem seaborn), PNGs a 300 dpi em `outputs/graficos/`.
- Paleta categórica validada para daltonismo; grid recessivo; rótulos diretos
  seletivos; eixos nomeados; layout ajustado (`tight_layout` + `bbox_inches`).

## 6. Relatório (`06_gerar_relatorio.py`)

- `outputs/relatorio_final.md` é montado programaticamente a partir das
  tabelas geradas — os números do relatório sempre refletem a última execução
  do pipeline.
