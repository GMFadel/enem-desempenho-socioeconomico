# Limitações do Estudo

## 1. Amostra, não população

A análise padrão usa as **primeiras 300.000 linhas** do arquivo de microdados
(~9% dos inscritos). Como a ordem das linhas do arquivo não é garantidamente
aleatória, a amostra pode não representar perfeitamente a população de
participantes. O pipeline permite reexecutar tudo na base completa
(`python 02_criar_amostra.py --completa`), e essa é a recomendação para
conclusões definitivas.

## 2. Associação não é causalidade

Nenhum resultado deste projeto permite afirmar que renda, tipo de escola ou
acesso à internet **causam** notas maiores ou menores. As variáveis
socioeconômicas são fortemente correlacionadas entre si (renda ↔ tipo de
escola ↔ escolaridade dos pais ↔ acesso à tecnologia), e as diferenças
apresentadas são **brutas**, sem controle de variáveis, pareamento ou testes
de significância.

## 3. Autodeclaração

As variáveis do questionário socioeconômico (Q001–Q025) e cor/raça são
autodeclaradas e podem conter erros ou omissões.

## 4. "Não respondeu" no tipo de escola

Mais da metade dos participantes da amostra não informa o tipo de escola
(`TP_ESCOLA = 1`, "Não respondeu"). A comparação pública x privada vale
apenas para quem respondeu, e esse subgrupo pode não ser representativo.

## 5. Seleção por presença

A base de desempenho considera apenas presentes nas 4 provas. Como a ausência
é maior nas faixas de renda mais baixas, as diferenças de nota entre grupos
tendem a ser **subestimadas** (os ausentes de baixa renda não entram na média).
Por isso a taxa de presença é analisada separadamente.

## 6. Treineiros

Treineiros (~7% da amostra) foram removidos da análise principal. Eles podem
ser objeto de análise própria, mas seus resultados não são comparáveis aos de
participantes regulares.

## 7. Médias por UF

Diferenças entre UFs refletem também a composição socioeconômica e a taxa de
participação de cada estado — não medem qualidade da educação local.

## 8. Privacidade

Os dados são públicos e o INEP os disponibiliza com adequações de
privacidade/LGPD (supressões e transformações). Nada aqui identifica
participantes individuais.
