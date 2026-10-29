-- Relatório 3 (junção + filtro): produtos abaixo do estoque mínimo e quem fornece
SELECT PRO.ID_PRODUTO                         AS CODIGO
     , PRO.NOME                               AS PRODUTO
     , PRO.QTD_ESTOQUE                        AS ESTOQUE_ATUAL
     , PRO.ESTOQUE_MINIMO                     AS ESTOQUE_MINIMO
     , PRO.ESTOQUE_MINIMO - PRO.QTD_ESTOQUE   AS FALTAM
     , FORN.RAZAO_SOCIAL                      AS FORNECEDOR
     , FORN.TELEFONE                          AS TELEFONE
  FROM PRODUTOS PRO
 INNER JOIN FORNECEDORES FORN ON PRO.ID_FORNECEDOR = FORN.ID_FORNECEDOR
 WHERE PRO.QTD_ESTOQUE < PRO.ESTOQUE_MINIMO
 ORDER BY FALTAM DESC
