from datetime import datetime

from conexion.oracle_queries import OracleQueries
from controller.entrada import ler_inteiro, confirmar
from model.compra import Compra
from model.fornecedor import Fornecedor


def ler_data(mensagem: str, atual: datetime = None) -> datetime:
    """Lê uma data no formato DD/MM/AAAA. ENTER usa a data atual do registro ou a data de hoje."""
    padrao = atual or datetime.now()
    while True:
        valor = input(f"{mensagem} [ENTER = {padrao.strftime('%d/%m/%Y')}]: ").strip()
        if valor == "":
            return padrao
        try:
            return datetime.strptime(valor, "%d/%m/%Y")
        except ValueError:
            print("Data inválida. Use o formato DD/MM/AAAA (ex.: 29/10/2026).")


def data_sql(data: datetime) -> str:
    return f"TO_DATE('{data.strftime('%d/%m/%Y')}', 'DD/MM/YYYY')"


class Controller_Compra:

    # ------------------------------------------------------------------
    # INSERIR (edital 6.b)
    # ------------------------------------------------------------------
    def inserir_compra(self) -> Compra:
        print("\n--- Nova compra ---")
        with OracleQueries() as oracle:
            self._listar_fornecedores(oracle)
            id_fornecedor = ler_inteiro("Código do fornecedor da compra", minimo=1)
            if not self._existe(oracle, "FORNECEDORES", f"ID_FORNECEDOR = {id_fornecedor}"):
                print(f"O fornecedor de código {id_fornecedor} não existe.")
                return None
            data = ler_data("Data da compra (DD/MM/AAAA)")

            oracle.write("INSERT INTO COMPRAS (ID_COMPRA, DATA_COMPRA, ID_FORNECEDOR) "
                         f"VALUES (COMPRAS_ID_SEQ.NEXTVAL, {data_sql(data)}, {id_fornecedor})")
            id_compra = oracle.query("SELECT COMPRAS_ID_SEQ.CURRVAL AS ID FROM DUAL")[0]["id"]
            compra = self.buscar(oracle, id_compra)

        print("\nCompra cadastrada com sucesso:")
        print(compra.to_string())
        print("Agora cadastre os produtos desta compra em: Inserir > Itens de Compra.")
        return compra

    # ------------------------------------------------------------------
    # ATUALIZAR (edital 6.d)
    # ------------------------------------------------------------------
    def atualizar_compra(self) -> Compra:
        with OracleQueries() as oracle:
            id_compra = ler_inteiro("\nCódigo da compra que deseja alterar", minimo=1)
            compra = self.buscar(oracle, id_compra)
            if compra is None:
                print(f"A compra de código {id_compra} não existe.")
                return None

            print("\nDados atuais:")
            print(compra.to_string())
            print("\nDigite os novos valores (ENTER mantém o valor atual):")
            data = ler_data("Data da compra (DD/MM/AAAA)", atual=compra.get_data_compra())

            # O fornecedor só pode mudar se a compra ainda não tem itens,
            # porque cada item precisa ser de um produto do fornecedor da compra
            id_fornecedor = compra.get_fornecedor().get_id_fornecedor()
            if self._existe(oracle, "ITENS_COMPRA", f"ID_COMPRA = {id_compra}"):
                print("(O fornecedor não pode ser alterado: esta compra já possui itens.)")
            else:
                self._listar_fornecedores(oracle)
                novo = ler_inteiro("Código do fornecedor", minimo=1, atual=id_fornecedor)
                if novo != id_fornecedor and not self._existe(oracle, "FORNECEDORES", f"ID_FORNECEDOR = {novo}"):
                    print(f"O fornecedor {novo} não existe. O fornecedor atual foi mantido.")
                else:
                    id_fornecedor = novo

            oracle.write(f"UPDATE COMPRAS SET DATA_COMPRA = {data_sql(data)}, "
                         f"ID_FORNECEDOR = {id_fornecedor} WHERE ID_COMPRA = {id_compra}")
            compra = self.buscar(oracle, id_compra)

        print("\nCompra atualizada:")
        print(compra.to_string())
        return compra

    # ------------------------------------------------------------------
    # REMOVER (edital 6.c)
    # ------------------------------------------------------------------
    def excluir_compra(self) -> bool:
        with OracleQueries() as oracle:
            id_compra = ler_inteiro("\nCódigo da compra que deseja remover", minimo=1)
            compra = self.buscar(oracle, id_compra)
            if compra is None:
                print(f"A compra de código {id_compra} não existe.")
                return False

            print(compra.to_string())
            if not confirmar("Deseja realmente remover esta compra?"):
                print("Remoção cancelada.")
                return "cancelado"   # volta ao menu principal (edital 6.c.5)

            comandos = []

            # (6.c.5.i) A compra é chave estrangeira em ITENS_COMPRA
            itens = oracle.query("SELECT ID_PRODUTO, QUANTIDADE FROM ITENS_COMPRA "
                                 f"WHERE ID_COMPRA = {id_compra}")
            if itens:
                print(f"\nAtenção: esta compra possui {len(itens)} item(ns).")
                if not confirmar("Deseja remover também os itens (o estoque dos produtos será reduzido)?"):
                    print("A compra não pode ser removida enquanto tiver itens.")
                    return False
                # Desfaz a entrada no estoque de cada produto (sem deixar negativo)
                for item in itens:
                    comandos.append(f"UPDATE PRODUTOS SET QTD_ESTOQUE = "
                                    f"GREATEST(QTD_ESTOQUE - {int(item['quantidade'])}, 0) "
                                    f"WHERE ID_PRODUTO = {item['id_produto']}")
                comandos.append(f"DELETE FROM ITENS_COMPRA WHERE ID_COMPRA = {id_compra}")

            comandos.append(f"DELETE FROM COMPRAS WHERE ID_COMPRA = {id_compra}")
            oracle.write_many(comandos)   # tudo numa transação

        print("\nCompra removida com sucesso:")
        print(compra.to_string())
        return True

    # ------------------------------------------------------------------
    # Funções de apoio
    # ------------------------------------------------------------------
    def buscar(self, oracle: OracleQueries, id_compra: int) -> Compra:
        linhas = oracle.query(
            "SELECT COM.ID_COMPRA, COM.DATA_COMPRA, FORN.ID_FORNECEDOR, FORN.RAZAO_SOCIAL, "
            "FORN.CNPJ, FORN.TELEFONE, FORN.EMAIL "
            "FROM COMPRAS COM "
            "INNER JOIN FORNECEDORES FORN ON COM.ID_FORNECEDOR = FORN.ID_FORNECEDOR "
            f"WHERE COM.ID_COMPRA = {id_compra}")
        if not linhas:
            return None
        c = linhas[0]
        fornecedor = Fornecedor(c["id_fornecedor"], c["razao_social"], c["cnpj"], c["telefone"], c["email"])
        return Compra(c["id_compra"], c["data_compra"], fornecedor)

    def _existe(self, oracle: OracleQueries, tabela: str, condicao: str) -> bool:
        return int(oracle.query(f"SELECT COUNT(1) AS TOTAL FROM {tabela} WHERE {condicao}")[0]["total"]) > 0

    def _listar_fornecedores(self, oracle: OracleQueries):
        print("\nFornecedores cadastrados:")
        for f in oracle.query("SELECT ID_FORNECEDOR, RAZAO_SOCIAL FROM FORNECEDORES ORDER BY ID_FORNECEDOR"):
            print(f"  {f['id_fornecedor']} - {f['razao_social']}")
