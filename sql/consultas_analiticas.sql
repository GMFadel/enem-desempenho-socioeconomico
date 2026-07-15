-- ============================================================================
-- Consultas analíticas — Fatores Socioeconômicos e Desempenho no ENEM 2022
--
-- Tabela de referência: enem_2022_tratado
-- (equivalente ao CSV outputs/tabelas/enem_2022_tratado.csv: sem treineiros,
--  apenas participantes presentes nas 4 provas objetivas)
--
-- Tabela auxiliar: enem_2022_base_presenca
-- (sem treineiros, INCLUI ausentes — usada para taxas de presença)
--
-- As consultas usam SQL padrão (testadas mentalmente contra DuckDB/PostgreSQL;
-- ajuste ROUND/limite conforme o dialeto).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Média geral por tipo de escola
--    (quantos participantes e qual a média de cada grupo)
-- ----------------------------------------------------------------------------
SELECT
    tipo_escola,
    COUNT(*)                    AS participantes,
    ROUND(AVG(media_geral), 2)  AS media_geral,
    ROUND(AVG(NU_NOTA_MT), 2)   AS media_matematica,
    ROUND(AVG(NU_NOTA_REDACAO), 2) AS media_redacao
FROM enem_2022_tratado
GROUP BY tipo_escola
ORDER BY media_geral DESC;

-- ----------------------------------------------------------------------------
-- 2. Média geral por faixa de renda familiar (Q006)
--    A coluna renda_familiar já vem rotulada com o prefixo da faixa (A..Q),
--    então a ordenação alfabética preserva a ordem crescente de renda.
-- ----------------------------------------------------------------------------
SELECT
    renda_familiar,
    COUNT(*)                   AS participantes,
    ROUND(AVG(media_geral), 2) AS media_geral
FROM enem_2022_tratado
GROUP BY renda_familiar
ORDER BY renda_familiar;

-- ----------------------------------------------------------------------------
-- 3. Média geral por UF de aplicação da prova
-- ----------------------------------------------------------------------------
SELECT
    SG_UF_PROVA                AS uf,
    COUNT(*)                   AS participantes,
    ROUND(AVG(media_geral), 2) AS media_geral
FROM enem_2022_tratado
GROUP BY SG_UF_PROVA
ORDER BY media_geral DESC;

-- ----------------------------------------------------------------------------
-- 4. Taxa de presença por faixa de renda
--    Usa a base COM ausentes; presente_todas é booleano (0/1).
--    A taxa mostra que a ausência é maior nas faixas de renda mais baixas.
-- ----------------------------------------------------------------------------
SELECT
    renda_familiar,
    COUNT(*)                                            AS inscritos,
    SUM(CASE WHEN presente_todas THEN 1 ELSE 0 END)     AS presentes_todas,
    ROUND(100.0 * SUM(CASE WHEN presente_todas THEN 1 ELSE 0 END)
          / COUNT(*), 2)                                AS taxa_presenca_pct
FROM enem_2022_base_presenca
GROUP BY renda_familiar
ORDER BY renda_familiar;

-- ----------------------------------------------------------------------------
-- 5. Top 10 UFs por média geral
-- ----------------------------------------------------------------------------
SELECT
    SG_UF_PROVA                AS uf,
    COUNT(*)                   AS participantes,
    ROUND(AVG(media_geral), 2) AS media_geral
FROM enem_2022_tratado
GROUP BY SG_UF_PROVA
ORDER BY media_geral DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Bônus: como carregar os CSVs no DuckDB para executar estas consultas
-- ----------------------------------------------------------------------------
-- CREATE TABLE enem_2022_tratado AS
--     SELECT * FROM read_csv_auto('outputs/tabelas/enem_2022_tratado.csv');
-- CREATE TABLE enem_2022_base_presenca AS
--     SELECT * FROM read_csv_auto('outputs/tabelas/enem_2022_base_presenca.csv');
