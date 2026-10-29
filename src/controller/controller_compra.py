from conexao import Conexao, sql_data
from model.compra import Compra
from model.fornecedor import Fornecedor


class ControllerCompra:
    def __init__(self, conexao: Conexao):
        self.conexao = conexao

    def existe(self, id_compra: int) -> bool:
        return self.conexao.valor("select count(1) total from compras "
                                  "where id_compra = " + str(id_compra)) > 0

    def inserir(self, c: Compra) -> bool:
        c.set_id_compra(self.conexao.valor("select seq_compras.nextval from dual"))
        self.conexao.executar(
            "insert into compras (id_compra, data_compra, id_fornecedor) values ("
            + str(c.get_id_compra()) + ", "
            + sql_data(c.get_data_compra()) + ", "
            + str(c.get_fornecedor().get_id_fornecedor()) + ")")
        return True

    def atualizar(self, c: Compra) -> bool:
        if not self.existe(c.get_id_compra()):
            print("Compra não encontrada.")
            return False
        atual = self.buscar(c.get_id_compra())
        trocou = (atual.get_fornecedor().get_id_fornecedor()
                  != c.get_fornecedor().get_id_fornecedor())
        if trocou and self.tem_filhos(c.get_id_compra()):
            print("Esta compra já possui itens; não é possível trocar o fornecedor.")
            return False
        self.conexao.executar(
            "update compras set data_compra = " + sql_data(c.get_data_compra())
            + ", id_fornecedor = " + str(c.get_fornecedor().get_id_fornecedor())
            + " where id_compra = " + str(c.get_id_compra()))
        return True

    def tem_filhos(self, id_compra: int) -> bool:
        """A compra é FK em ITENS_COMPRA?"""
        return self.conexao.valor("select count(1) total from itens_compra "
                                  "where id_compra = " + str(id_compra)) > 0

    def remover(self, id_compra: int, apagar_filhos: bool = False) -> bool:
        if not self.existe(id_compra):
            print("Compra não encontrada.")
            return False
        if self.tem_filhos(id_compra) and not apagar_filhos:
            print("Esta compra possui itens e não pode ser excluída.")
            return False
        i = str(id_compra)
        self.conexao.executar("delete from itens_compra where id_compra = " + i,
                              "delete from compras where id_compra = " + i)
        return True

    def listar(self):
        return self.conexao.consultar(
            "select c.id_compra, to_char(c.data_compra, 'DD/MM/YYYY'), f.razao_social "
            "from compras c inner join fornecedores f on f.id_fornecedor = c.id_fornecedor "
            "order by c.id_compra")

    def buscar(self, id_compra: int):
        linhas = self.conexao.consultar(
            "select c.id_compra, c.data_compra, f.id_fornecedor, f.razao_social, f.cnpj "
            "from compras c inner join fornecedores f on f.id_fornecedor = c.id_fornecedor "
            "where c.id_compra = " + str(id_compra))
        if not linhas:
            return None
        r = linhas[0]
        return Compra(r[0], r[1], Fornecedor(r[2], r[3], r[4]))
