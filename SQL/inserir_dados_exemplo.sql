/* =====================================================================
   SISTEMA DE CONTROLE DE ESTOQUE
   Dados de exemplo para testes
   Executar DEPOIS do criar_tabelas.sql, com as tabelas vazias
   (os códigos 1, 2, 3... dependem das sequences começarem em 1).

   Obs.: aqui a QTD_ESTOQUE de cada produto já vem informada.
   O ajuste automático do estoque acontece só quando o item de compra
   é cadastrado pelo programa em Python.
   ===================================================================== */

/* ---------- FORNECEDORES (5) ----------
   Colunas: ID, RAZAO_SOCIAL, CNPJ, TELEFONE, EMAIL */
INSERT INTO FORNECEDORES VALUES (FORNECEDORES_ID_SEQ.NEXTVAL, 'Distribuidora Capixaba de Alimentos LTDA', '12345678000101', '2733451200', 'vendas@capixabaalimentos.com.br');
INSERT INTO FORNECEDORES VALUES (FORNECEDORES_ID_SEQ.NEXTVAL, 'Limpeza Total Produtos de Higiene ME',     '23456789000102', '2799881234', 'comercial@limpezatotal.com.br');
INSERT INTO FORNECEDORES VALUES (FORNECEDORES_ID_SEQ.NEXTVAL, 'Bebidas Serra Azul S.A.',                  '34567890000103', '2733216500', 'pedidos@serraazul.com.br');
INSERT INTO FORNECEDORES VALUES (FORNECEDORES_ID_SEQ.NEXTVAL, 'Papelaria e Embalagens Cariacica LTDA',    '45678901000104', '2733367711', 'vendas@embalagenscariacica.com.br');
INSERT INTO FORNECEDORES VALUES (FORNECEDORES_ID_SEQ.NEXTVAL, 'Hortifruti Montanhas Capixabas LTDA',      '56789012000105', '2832541090', NULL);

/* ---------- PRODUTOS (12) ----------
   Colunas: ID, NOME, CATEGORIA, UNIDADE_MEDIDA, PRECO_CUSTO, QTD_ESTOQUE, ESTOQUE_MINIMO, ID_FORNECEDOR
   Os marcados com "BAIXO" estão abaixo do estoque mínimo (aparecem no relatório de estoque baixo). */
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Arroz Tipo 1 5kg',              'Alimentos',  'PCT',  22.90, 120,  50, 1);
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Feijão Preto 1kg',              'Alimentos',  'PCT',   7.50,  18,  40, 1); -- BAIXO
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Café Torrado 500g',             'Alimentos',  'PCT',  16.40,  12,  25, 1); -- BAIXO
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Detergente Neutro 500ml',       'Limpeza',    'UN',    1.90, 200,  80, 2);
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Água Sanitária 2L',             'Limpeza',    'UN',    4.30,  22,  50, 2); -- BAIXO
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Sabão em Pó 1kg',               'Limpeza',    'CX',   11.70,  45,  40, 2);
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Refrigerante Cola 2L',          'Bebidas',    'UN',    5.60, 150,  60, 3);
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Água Mineral 500ml (fardo 12)', 'Bebidas',    'FD',   10.20,   8,  30, 3); -- BAIXO
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Suco de Uva Integral 1L',       'Bebidas',    'UN',    9.90,  35,  20, 3);
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Caixa de Papelão Média',        'Embalagens', 'UN',    2.10, 300, 100, 4);
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Fita Adesiva 48mm',             'Embalagens', 'RL',    3.80,  15,  40, 4); -- BAIXO
INSERT INTO PRODUTOS VALUES (PRODUTOS_ID_SEQ.NEXTVAL, 'Banana Prata',                  'Hortifruti', 'KG',    3.50,  40,  20, 5);

/* ---------- COMPRAS (8) ----------
   Colunas: ID, DATA_COMPRA, ID_FORNECEDOR */
INSERT INTO COMPRAS VALUES (COMPRAS_ID_SEQ.NEXTVAL, TO_DATE('05/08/2026','DD/MM/YYYY'), 1);
INSERT INTO COMPRAS VALUES (COMPRAS_ID_SEQ.NEXTVAL, TO_DATE('03/09/2026','DD/MM/YYYY'), 2);
INSERT INTO COMPRAS VALUES (COMPRAS_ID_SEQ.NEXTVAL, TO_DATE('11/09/2026','DD/MM/YYYY'), 3);
INSERT INTO COMPRAS VALUES (COMPRAS_ID_SEQ.NEXTVAL, TO_DATE('22/09/2026','DD/MM/YYYY'), 4);
INSERT INTO COMPRAS VALUES (COMPRAS_ID_SEQ.NEXTVAL, TO_DATE('25/09/2026','DD/MM/YYYY'), 5);
INSERT INTO COMPRAS VALUES (COMPRAS_ID_SEQ.NEXTVAL, TO_DATE('01/10/2026','DD/MM/YYYY'), 1);
INSERT INTO COMPRAS VALUES (COMPRAS_ID_SEQ.NEXTVAL, TO_DATE('08/10/2026','DD/MM/YYYY'), 3);
INSERT INTO COMPRAS VALUES (COMPRAS_ID_SEQ.NEXTVAL, TO_DATE('20/10/2026','DD/MM/YYYY'), 2);

/* ---------- ITENS_COMPRA (18) ----------
   Colunas: ID_COMPRA, ID_PRODUTO, QUANTIDADE, PRECO_UNITARIO
   Regra: cada compra só tem produtos do mesmo fornecedor da compra. */
-- Compra 1 (Distribuidora Capixaba)
INSERT INTO ITENS_COMPRA VALUES (1,  1, 100, 22.50);
INSERT INTO ITENS_COMPRA VALUES (1,  2,  80,  7.30);
INSERT INTO ITENS_COMPRA VALUES (1,  3,  40, 16.00);
-- Compra 2 (Limpeza Total)
INSERT INTO ITENS_COMPRA VALUES (2,  4, 150,  1.85);
INSERT INTO ITENS_COMPRA VALUES (2,  5,  60,  4.20);
INSERT INTO ITENS_COMPRA VALUES (2,  6,  40, 11.50);
-- Compra 3 (Bebidas Serra Azul)
INSERT INTO ITENS_COMPRA VALUES (3,  7, 120,  5.40);
INSERT INTO ITENS_COMPRA VALUES (3,  8,  30, 10.00);
INSERT INTO ITENS_COMPRA VALUES (3,  9,  30,  9.80);
-- Compra 4 (Embalagens Cariacica)
INSERT INTO ITENS_COMPRA VALUES (4, 10, 250,  2.05);
INSERT INTO ITENS_COMPRA VALUES (4, 11,  50,  3.70);
-- Compra 5 (Hortifruti)
INSERT INTO ITENS_COMPRA VALUES (5, 12,  60,  3.40);
-- Compra 6 (Distribuidora Capixaba)
INSERT INTO ITENS_COMPRA VALUES (6,  1,  40, 22.90);
INSERT INTO ITENS_COMPRA VALUES (6,  3,  20, 16.40);
-- Compra 7 (Bebidas Serra Azul)
INSERT INTO ITENS_COMPRA VALUES (7,  7,  80,  5.60);
INSERT INTO ITENS_COMPRA VALUES (7,  9,  15,  9.90);
-- Compra 8 (Limpeza Total)
INSERT INTO ITENS_COMPRA VALUES (8,  4, 100,  1.90);
INSERT INTO ITENS_COMPRA VALUES (8,  6,  25, 11.70);

COMMIT;
