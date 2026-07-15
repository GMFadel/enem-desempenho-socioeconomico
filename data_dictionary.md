# Dicionário de Dados — variáveis usadas no projeto

Fonte: dicionário oficial `DICIONÁRIO/Dicionário_Microdados_Enem_2022.xlsx`
(aba MICRODADOS_ENEM_2022). Todos os códigos abaixo foram conferidos no
arquivo oficial do INEP.

## Identificação e perfil

| Variável | Descrição |
|---|---|
| `NU_INSCRICAO` | Número de inscrição (tratado como **texto** para evitar notação científica) |
| `NU_ANO` | Ano do ENEM (2022) |
| `TP_FAIXA_ETARIA` | Faixa etária (1 = menor de 17 anos ... 20 = maior de 70 anos) |
| `TP_SEXO` | Sexo (M/F) |
| `TP_COR_RACA` | Cor/raça: 0 Não declarado, 1 Branca, 2 Preta, 3 Parda, 4 Amarela, 5 Indígena, 6 Não dispõe da informação |
| `TP_ST_CONCLUSAO` | Situação do Ensino Médio: 1 já concluiu, 2 conclui em 2022, 3 conclui após 2022, 4 não cursa nem concluiu |
| `TP_ESCOLA` | Tipo de escola do EM: 1 Não respondeu, 2 Pública, 3 Privada |
| `TP_ENSINO` | Tipo de instituição: 1 Ensino Regular, 2 Educação Especial (substitutiva) |
| `IN_TREINEIRO` | 1 = fez a prova apenas para treinar, 0 = não |
| `SG_UF_PROVA` | UF de aplicação da prova |
| `NO_MUNICIPIO_PROVA` | Município de aplicação da prova |

## Presença e notas

| Variável | Descrição |
|---|---|
| `TP_PRESENCA_CN/CH/LC/MT` | 0 Faltou à prova, 1 Presente, 2 Eliminado |
| `NU_NOTA_CN` | Nota de Ciências da Natureza |
| `NU_NOTA_CH` | Nota de Ciências Humanas |
| `NU_NOTA_LC` | Nota de Linguagens e Códigos |
| `NU_NOTA_MT` | Nota de Matemática |
| `NU_NOTA_REDACAO` | Nota da Redação (0 a 1000) |

## Questionário socioeconômico

### Q001 / Q002 — Até que série seu pai / sua mãe estudou?

| Código | Significado |
|---|---|
| A | Nunca estudou |
| B | Não completou a 4ª série/5º ano do Ensino Fundamental |
| C | Completou a 4ª série/5º ano, mas não a 8ª série/9º ano do EF |
| D | Completou a 8ª série/9º ano do EF, mas não o Ensino Médio |
| E | Completou o Ensino Médio, mas não a Faculdade |
| F | Completou a Faculdade, mas não a Pós-graduação |
| G | Completou a Pós-graduação |
| H | Não sei |

### Q005 — Quantas pessoas moram na sua residência?

Valores de 1 (mora sozinho) a 20.

### Q006 — Renda mensal da família (salário mínimo 2022 = R$ 1.212)

| Código | Faixa | Código | Faixa |
|---|---|---|---|
| A | Nenhuma renda | J | R$ 7.272,01 – 8.484,00 |
| B | Até R$ 1.212,00 | K | R$ 8.484,01 – 9.696,00 |
| C | R$ 1.212,01 – 1.818,00 | L | R$ 9.696,01 – 10.908,00 |
| D | R$ 1.818,01 – 2.424,00 | M | R$ 10.908,01 – 12.120,00 |
| E | R$ 2.424,01 – 3.030,00 | N | R$ 12.120,01 – 14.544,00 |
| F | R$ 3.030,01 – 3.636,00 | O | R$ 14.544,01 – 18.180,00 |
| G | R$ 3.636,01 – 4.848,00 | P | R$ 18.180,01 – 24.240,00 |
| H | R$ 4.848,01 – 6.060,00 | Q | Acima de R$ 24.240,00 |
| I | R$ 6.060,01 – 7.272,00 | | |

### Q024 — Na sua residência tem computador?

| Código | Significado |
|---|---|
| A | Não |
| B | Sim, um |
| C | Sim, dois |
| D | Sim, três |
| E | Sim, quatro ou mais |

### Q025 — Na sua residência tem acesso à Internet?

| Código | Significado |
|---|---|
| A | Não |
| B | Sim |

## Variáveis derivadas (criadas em `src/03_tratar_dados.py`)

| Variável | Definição |
|---|---|
| `presente_todas` | `True` se `TP_PRESENCA_* == 1` nas 4 provas objetivas |
| `media_objetivas` | Média das 4 provas objetivas (CN, CH, LC, MT) |
| `media_geral` | Média das 4 objetivas + Redação |
| `tipo_escola`, `cor_raca`, `treineiro`, `escolaridade_pai`, `escolaridade_mae`, `renda_familiar`, `computador_casa`, `internet_casa` | Versões legíveis dos códigos acima |
