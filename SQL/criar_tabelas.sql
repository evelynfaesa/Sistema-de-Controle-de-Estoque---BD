/* =====================================================================
   SISTEMA DE CONTROLE DE ESTOQUE
   Script de criação: sequences, tabelas e relacionamentos (Oracle)
   Disciplina: Banco de Dados 2026/2 - Prof. Howard Roatti

   Executar conectado ao usuário do banco (na VM: labdatabase).
   Para recriar tudo do zero, descomente os DROP abaixo e execute de novo.
   ===================================================================== */

/* ---------- Apaga tudo (descomente para recriar) ----------
DROP TABLE ITENS_COMPRA;
DROP TABLE COMPRAS;
DROP TABLE PRODUTOS;
DROP TABLE FORNECEDORES;
DROP SEQUENCE FORNECEDORES_ID_SEQ;
DROP SEQUENCE PRODUTOS_ID_SEQ;
DROP SEQUENCE COMPRAS_ID_SEQ;
------------------------------------------------------------- */

/* ---------- Sequences: geram os códigos automaticamente ---------- */
CREATE SEQUENCE FORNECEDORES_ID_SEQ START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE PRODUTOS_ID_SEQ     START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE COMPRAS_ID_SEQ      START WITH 1 INCREMENT BY 1;

/* ---------- FORNECEDORES: quem vende para a empresa ---------- */
CREATE TABLE FORNECEDORES (
    ID_FORNECEDOR   NUMBER          NOT NULL,
    RAZAO_SOCIAL    VARCHAR2(100)   NOT NULL,
    CNPJ            CHAR(14)        NOT NULL,
    TELEFONE        VARCHAR2(15),
    EMAIL           VARCHAR2(100),
    CONSTRAINT FORNECEDORES_PK      PRIMARY KEY (ID_FORNECEDOR),
    CONSTRAINT FORNECEDORES_CNPJ_UK UNIQUE (CNPJ)
);

/* ---------- PRODUTOS: o que existe no estoque ---------- */
CREATE TABLE PRODUTOS (
    ID_PRODUTO      NUMBER          NOT NULL,
    NOME            VARCHAR2(100)   NOT NULL,
    CATEGORIA       VARCHAR2(50)    NOT NULL,
    UNIDADE_MEDIDA  VARCHAR2(10)    NOT NULL,
    PRECO_CUSTO     NUMBER(10,2)    NOT NULL,
    QTD_ESTOQUE     NUMBER          DEFAULT 0 NOT NULL,
    ESTOQUE_MINIMO  NUMBER          NOT NULL,
    ID_FORNECEDOR   NUMBER          NOT NULL,
    CONSTRAINT PRODUTOS_PK          PRIMARY KEY (ID_PRODUTO),
    CONSTRAINT PRODUTOS_PRECO_CK    CHECK (PRECO_CUSTO > 0),
    CONSTRAINT PRODUTOS_QTD_CK      CHECK (QTD_ESTOQUE >= 0),
    CONSTRAINT PRODUTOS_MINIMO_CK   CHECK (ESTOQUE_MINIMO >= 0),
    CONSTRAINT FORNECEDORES_PRODUTOS_FK FOREIGN KEY (ID_FORNECEDOR)
        REFERENCES FORNECEDORES (ID_FORNECEDOR)
);

/* ---------- COMPRAS: o "cabeçalho" da compra (como uma nota fiscal) ---------- */
CREATE TABLE COMPRAS (
    ID_COMPRA       NUMBER          NOT NULL,
    DATA_COMPRA     DATE            DEFAULT SYSDATE NOT NULL,
    ID_FORNECEDOR   NUMBER          NOT NULL,
    CONSTRAINT COMPRAS_PK           PRIMARY KEY (ID_COMPRA),
    CONSTRAINT FORNECEDORES_COMPRAS_FK FOREIGN KEY (ID_FORNECEDOR)
        REFERENCES FORNECEDORES (ID_FORNECEDOR)
);

/* ---------- ITENS_COMPRA: as linhas da nota (produto, quantidade, preço) ----------
   Resolve a relação N:N entre COMPRAS e PRODUTOS.
   Chave primária composta: um produto aparece uma única vez em cada compra. */
CREATE TABLE ITENS_COMPRA (
    ID_COMPRA       NUMBER          NOT NULL,
    ID_PRODUTO      NUMBER          NOT NULL,
    QUANTIDADE      NUMBER          NOT NULL,
    PRECO_UNITARIO  NUMBER(10,2)    NOT NULL,
    CONSTRAINT ITENS_COMPRA_PK      PRIMARY KEY (ID_COMPRA, ID_PRODUTO),
    CONSTRAINT ITENS_QTD_CK         CHECK (QUANTIDADE > 0),
    CONSTRAINT ITENS_PRECO_CK       CHECK (PRECO_UNITARIO > 0),
    CONSTRAINT COMPRAS_ITENS_FK FOREIGN KEY (ID_COMPRA)
        REFERENCES COMPRAS (ID_COMPRA),
    CONSTRAINT PRODUTOS_ITENS_FK FOREIGN KEY (ID_PRODUTO)
        REFERENCES PRODUTOS (ID_PRODUTO)
);
