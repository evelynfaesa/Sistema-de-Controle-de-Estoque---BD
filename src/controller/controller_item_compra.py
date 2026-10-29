from conexion.oracle_queries import OracleQueries
from controller.controller_compra import Controller_Compra
from controller.entrada import ler_inteiro, ler_decimal, confirmar
from model.item_compra import ItemCompra
from model.produto import Produto


class Controller_Item_Compra:
    """Itens de compra. Toda inclusão, alteração ou remoção de item
    ajusta automaticamente o estoque do produto (QTD_ESTOQUE)."""

    def __init__(self):
        self.ctrl_compra = Controller_Compra()

    # ------------------------------------------------------------------
    # INSERIR (edital 6.b)
    # ------------------------------------------------------------------
    def inserir_item_compra(self) -> ItemCompra:
        print("\n--- Novo item de compra ---")
        with OracleQueries() as oracle:
            self._listar_compras(oracle)
            id_compra = ler_inteiro("Código da compra", minimo=1)
            compra = self.ctrl_compra.buscar(oracle, id_compra)
            if compra is None:
                print(f"A compra de código {id_compra} não existe. Cadastre a compra primeiro.")
                return None

            # Regra: a compra só aceita produtos do fornecedor dela
            id_fornecedor = compra.get_fornecedor().get_id_fornecedor()
            produtos = oracle.query("SELECT ID_PRODUTO, NOME, PRECO_CUSTO FROM PRODUTOS "
                                    f"WHERE ID_FORNECEDOR = {id_fornecedor} ORDER BY NOME")
            if not produtos:
                print("Este fornecedor não possui produtos cadastrados.")
                return None
            print(f"\nProdutos de {compra.get_fornecedor().get_razao_social()}:")
            for p in produtos:
                print(f"  {p['id_produto']} - {p['nome']} (custo R$ {float(p['preco_custo']):.2f})")

            id_produto = ler_inteiro("Código do produto", minimo=1)
            produto = next((p for p in produtos if p["id_produto"] == id_produto), None)
            if produto is None:
                print("Este produto não pertence ao fornecedor da compra.")
                return None
            if self._existe(oracle, id_compra, id_produto):
                print("Este produto já está nesta compra. Use Atualizar para mudar a quantidade.")
                return None

            quantidade = ler_inteiro("Quantidade comprada", minimo=1)
            preco = ler_decimal("Preço unitário (R$)")

            # Insere o item e soma a quantidade ao estoque, na mesma transação
            oracle.write_many([
                "INSERT INTO ITENS_COMPRA (ID_COMPRA, ID_PRODUTO, QUANTIDADE, PRECO_UNITARIO) "
                f"VALUES ({id_compra}, {id_produto}, {quantidade}, {preco})",
                f"UPDATE PRODUTOS SET QTD_ESTOQUE = QTD_ESTOQUE + {quantidade} WHERE ID_PRODUTO = {id_produto}",
            ])
            item = self._buscar(oracle, id_compra, id_produto)

        print("\nItem cadastrado com sucesso (estoque atualizado):")
        print(item.to_string())
        print(f"Estoque atual do produto: {item.get_produto().get_qtd_estoque()}")
        return item

    # ------------------------------------------------------------------
    # ATUALIZAR (edital 6.d)
    # ------------------------------------------------------------------
    def atualizar_item_compra(self) -> ItemCompra:
        with OracleQueries() as oracle:
            id_compra = ler_inteiro("\nCódigo da compra do item", minimo=1)
            id_produto = ler_inteiro("Código do produto do item", minimo=1)
            item = self._buscar(oracle, id_compra, id_produto)
            if item is None:
                print("Este item não existe (confira os códigos na listagem acima).")
                return None

            print("\nDados atuais:")
            print(item.to_string())
            print("\nDigite os novos valores (ENTER mantém o valor atual):")
            quantidade = ler_inteiro("Quantidade comprada", minimo=1, atual=item.get_quantidade())
            preco = ler_decimal("Preço unitário (R$)", atual=item.get_preco_unitario())

            # Ajusta o estoque pela diferença entre a quantidade nova e a antiga
            diferenca = quantidade - item.get_quantidade()
            oracle.write_many([
                f"UPDATE ITENS_COMPRA SET QUANTIDADE = {quantidade}, PRECO_UNITARIO = {preco} "
                f"WHERE ID_COMPRA = {id_compra} AND ID_PRODUTO = {id_produto}",
                f"UPDATE PRODUTOS SET QTD_ESTOQUE = GREATEST(QTD_ESTOQUE + ({diferenca}), 0) "
                f"WHERE ID_PRODUTO = {id_produto}",
            ])
            item = self._buscar(oracle, id_compra, id_produto)

        print("\nItem atualizado (estoque ajustado):")
        print(item.to_string())
        print(f"Estoque atual do produto: {item.get_produto().get_qtd_estoque()}")
        return item

    # ------------------------------------------------------------------
    # REMOVER (edital 6.c) - ITENS_COMPRA não é referenciada por nenhuma tabela
    # ------------------------------------------------------------------
    def excluir_item_compra(self) -> bool:
        with OracleQueries() as oracle:
            id_compra = ler_inteiro("\nCódigo da compra do item", minimo=1)
            id_produto = ler_inteiro("Código do produto do item", minimo=1)
            item = self._buscar(oracle, id_compra, id_produto)
            if item is None:
                print("Este item não existe (confira os códigos na listagem acima).")
                return False

            print(item.to_string())
            if not confirmar("Deseja realmente remover este item (o estoque do produto será reduzido)?"):
                print("Remoção cancelada.")
                return "cancelado"   # volta ao menu principal (edital 6.c.5)

            oracle.write_many([
                f"UPDATE PRODUTOS SET QTD_ESTOQUE = GREATEST(QTD_ESTOQUE - {item.get_quantidade()}, 0) "
                f"WHERE ID_PRODUTO = {id_produto}",
                f"DELETE FROM ITENS_COMPRA WHERE ID_COMPRA = {id_compra} AND ID_PRODUTO = {id_produto}",
            ])

        print("\nItem removido com sucesso:")
        print(item.to_string())
        return True

    # ------------------------------------------------------------------
    # Funções de apoio
    # ------------------------------------------------------------------
    def _existe(self, oracle: OracleQueries, id_compra: int, id_produto: int) -> bool:
        return int(oracle.query("SELECT COUNT(1) AS TOTAL FROM ITENS_COMPRA "
                                f"WHERE ID_COMPRA = {id_compra} AND ID_PRODUTO = {id_produto}")[0]["total"]) > 0

    def _listar_compras(self, oracle: OracleQueries):
        print("\nCompras cadastradas:")
        for c in oracle.query("SELECT COM.ID_COMPRA, COM.DATA_COMPRA, FORN.RAZAO_SOCIAL "
                              "FROM COMPRAS COM INNER JOIN FORNECEDORES FORN "
                              "ON COM.ID_FORNECEDOR = FORN.ID_FORNECEDOR ORDER BY COM.ID_COMPRA"):
            data = c["data_compra"].strftime("%d/%m/%Y") if hasattr(c["data_compra"], "strftime") else c["data_compra"]
            print(f"  {c['id_compra']} - {data} - {c['razao_social']}")

    def _buscar(self, oracle: OracleQueries, id_compra: int, id_produto: int) -> ItemCompra:
        linhas = oracle.query(
            "SELECT ITE.QUANTIDADE, ITE.PRECO_UNITARIO, PRO.ID_PRODUTO, PRO.NOME, PRO.CATEGORIA, "
            "PRO.UNIDADE_MEDIDA, PRO.PRECO_CUSTO, PRO.QTD_ESTOQUE, PRO.ESTOQUE_MINIMO "
            "FROM ITENS_COMPRA ITE "
            "INNER JOIN PRODUTOS PRO ON ITE.ID_PRODUTO = PRO.ID_PRODUTO "
            f"WHERE ITE.ID_COMPRA = {id_compra} AND ITE.ID_PRODUTO = {id_produto}")
        if not linhas:
            return None
        i = linhas[0]
        compra = self.ctrl_compra.buscar(oracle, id_compra)
        produto = Produto(i["id_produto"], i["nome"], i["categoria"], i["unidade_medida"],
                          float(i["preco_custo"]), int(i["qtd_estoque"]), int(i["estoque_minimo"]),
                          compra.get_fornecedor())
        return ItemCompra(compra, produto, int(i["quantidade"]), float(i["preco_unitario"]))
