from conexao import Conexao, sql_decimal
from model.compra import Compra
from model.fornecedor import Fornecedor
from model.item_compra import ItemCompra
from model.produto import Produto


class ControllerItemCompra:
    """ITENS_COMPRA tem PK composta (id_compra, id_produto)."""

    def __init__(self, conexao: Conexao):
        self.conexao = conexao

    def existe(self, id_compra: int, id_produto: int) -> bool:
        return self.conexao.valor(
            "select count(1) total from itens_compra where id_compra = " + str(id_compra)
            + " and id_produto = " + str(id_produto)) > 0

    def produto_pertence_ao_fornecedor_da_compra(self, id_compra: int, id_produto: int) -> bool:
        return self.conexao.valor(
            "select count(1) total from produtos p inner join compras c "
            "on c.id_fornecedor = p.id_fornecedor where p.id_produto = " + str(id_produto)
            + " and c.id_compra = " + str(id_compra)) > 0

    def inserir(self, item: ItemCompra) -> bool:
        id_compra = item.get_compra().get_id_compra()
        id_produto = item.get_produto().get_id_produto()
        if self.existe(id_compra, id_produto):
            print("Este produto já está nesta compra. Use a opção Atualizar.")
            return False
        if not self.produto_pertence_ao_fornecedor_da_compra(id_compra, id_produto):
            print("O produto não pertence ao fornecedor desta compra.")
            return False
        self.conexao.executar(
            "insert into itens_compra (id_compra, id_produto, quantidade, preco_unitario) values ("
            + str(id_compra) + ", " + str(id_produto) + ", "
            + str(item.get_quantidade()) + ", "
            + sql_decimal(item.get_preco_unitario()) + ")")
        return True

    def atualizar(self, item: ItemCompra) -> bool:
        id_compra = item.get_compra().get_id_compra()
        id_produto = item.get_produto().get_id_produto()
        if not self.existe(id_compra, id_produto):
            print("Item não encontrado.")
            return False
        self.conexao.executar(
            "update itens_compra set quantidade = " + str(item.get_quantidade())
            + ", preco_unitario = " + sql_decimal(item.get_preco_unitario())
            + " where id_compra = " + str(id_compra) + " and id_produto = " + str(id_produto))
        return True

    def tem_filhos(self, id_compra: int, id_produto: int) -> bool:
        """Item não é FK em nenhuma outra tabela."""
        return False

    def remover(self, id_compra: int, id_produto: int, apagar_filhos: bool = False) -> bool:
        if not self.existe(id_compra, id_produto):
            print("Item não encontrado.")
            return False
        self.conexao.executar(
            "delete from itens_compra where id_compra = " + str(id_compra)
            + " and id_produto = " + str(id_produto))
        return True

    def listar(self):
        return self.conexao.consultar(
            "select i.id_compra, i.id_produto, p.nome, i.quantidade "
            "from itens_compra i inner join produtos p on p.id_produto = i.id_produto "
            "order by i.id_compra, i.id_produto")

    def buscar(self, id_compra: int, id_produto: int):
        linhas = self.conexao.consultar(
            "select i.id_compra, c.data_compra, f.id_fornecedor, f.razao_social, "
            "i.id_produto, p.nome, i.quantidade, i.preco_unitario "
            "from itens_compra i "
            "inner join compras c on c.id_compra = i.id_compra "
            "inner join fornecedores f on f.id_fornecedor = c.id_fornecedor "
            "inner join produtos p on p.id_produto = i.id_produto "
            "where i.id_compra = " + str(id_compra) + " and i.id_produto = " + str(id_produto))
        if not linhas:
            return None
        r = linhas[0]
        compra = Compra(r[0], r[1], Fornecedor(r[2], r[3]))
        produto = Produto(id_produto=r[4], nome=r[5])
        return ItemCompra(compra, produto, r[6], r[7])
