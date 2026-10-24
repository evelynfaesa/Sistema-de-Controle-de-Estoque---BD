from conexion.oracle_queries import OracleQueries, escapar
from controller.entrada import ler_texto, ler_inteiro, confirmar
from model.fornecedor import Fornecedor


def texto_sql(valor) -> str:
    """Transforma um valor Python em texto SQL: None vira NULL, o resto vira 'texto'."""
    return "NULL" if valor is None else f"'{escapar(valor)}'"


class Controller_Fornecedor:

    # ------------------------------------------------------------------
    # INSERIR (edital 6.b)
    # ------------------------------------------------------------------
    def inserir_fornecedor(self) -> Fornecedor:
        print("\n--- Novo fornecedor ---")
        with OracleQueries() as oracle:
            cnpj = self._ler_cnpj()
            if self.existe_cnpj(oracle, cnpj):
                print(f"Já existe um fornecedor com o CNPJ {cnpj}.")
                return None

            razao_social = ler_texto("Razão social", tamanho_max=100)
            telefone = ler_texto("Telefone (opcional)", obrigatorio=False, tamanho_max=15)
            email = ler_texto("E-mail (opcional)", obrigatorio=False, tamanho_max=100)

            # Monta o INSERT concatenando os valores digitados (sem ORM, conforme o edital)
            sql = ("INSERT INTO FORNECEDORES (ID_FORNECEDOR, RAZAO_SOCIAL, CNPJ, TELEFONE, EMAIL) "
                   "VALUES (FORNECEDORES_ID_SEQ.NEXTVAL, "
                   f"{texto_sql(razao_social)}, '{cnpj}', {texto_sql(telefone)}, {texto_sql(email)})")
            oracle.write(sql)

            # O CNPJ é único, então serve para buscar o registro recém-criado
            fornecedor = self._buscar(oracle, f"CNPJ = '{cnpj}'")

        print("\nFornecedor cadastrado com sucesso:")
        print(fornecedor.to_string())
        return fornecedor

    # ------------------------------------------------------------------
    # ATUALIZAR (edital 6.d)
    # ------------------------------------------------------------------
    def atualizar_fornecedor(self) -> Fornecedor:
        with OracleQueries() as oracle:
            id_fornecedor = ler_inteiro("\nCódigo do fornecedor que deseja alterar", minimo=1)
            fornecedor = self._buscar(oracle, f"ID_FORNECEDOR = {id_fornecedor}")
            if fornecedor is None:
                print(f"O fornecedor de código {id_fornecedor} não existe.")
                return None

            print("\nDados atuais:")
            print(fornecedor.to_string())
            print("\nDigite os novos valores (ENTER mantém o valor atual):")

            razao_social = ler_texto("Razão social", tamanho_max=100, atual=fornecedor.get_razao_social())
            telefone = ler_texto("Telefone", obrigatorio=False, tamanho_max=15,
                                 atual=fornecedor.get_telefone() or "")
            email = ler_texto("E-mail", obrigatorio=False, tamanho_max=100,
                              atual=fornecedor.get_email() or "")

            sql = (f"UPDATE FORNECEDORES "
                   f"SET RAZAO_SOCIAL = {texto_sql(razao_social)}, "
                   f"TELEFONE = {texto_sql(telefone or None)}, "
                   f"EMAIL = {texto_sql(email or None)} "
                   f"WHERE ID_FORNECEDOR = {id_fornecedor}")
            oracle.write(sql)

            fornecedor = self._buscar(oracle, f"ID_FORNECEDOR = {id_fornecedor}")

        print("\nFornecedor atualizado:")
        print(fornecedor.to_string())
        return fornecedor

    # ------------------------------------------------------------------
    # REMOVER (edital 6.c)
    # ------------------------------------------------------------------
    def excluir_fornecedor(self) -> bool:
        with OracleQueries() as oracle:
            id_fornecedor = ler_inteiro("\nCódigo do fornecedor que deseja remover", minimo=1)
            fornecedor = self._buscar(oracle, f"ID_FORNECEDOR = {id_fornecedor}")
            if fornecedor is None:
                print(f"O fornecedor de código {id_fornecedor} não existe.")
                return False

            print(fornecedor.to_string())
            if not confirmar("Deseja realmente remover este fornecedor?"):
                print("Remoção cancelada.")
                return False

            comandos = []

            # (6.c.5.i) Verifica se o fornecedor é chave estrangeira em outras tabelas
            qtd_produtos = self._contar(oracle, "PRODUTOS", f"ID_FORNECEDOR = {id_fornecedor}")
            qtd_compras = self._contar(oracle, "COMPRAS", f"ID_FORNECEDOR = {id_fornecedor}")

            if qtd_produtos > 0 or qtd_compras > 0:
                print(f"\nAtenção: este fornecedor possui {qtd_produtos} produto(s) e "
                      f"{qtd_compras} compra(s) cadastrados.")
                if not confirmar("Deseja remover também esses registros e os itens de compra ligados a eles?"):
                    print("O fornecedor não pode ser removido enquanto tiver registros ligados a ele.")
                    return False

                # Remove na ordem certa: primeiro as tabelas filhas, depois a mãe
                comandos += [
                    f"DELETE FROM ITENS_COMPRA WHERE ID_COMPRA IN "
                    f"(SELECT ID_COMPRA FROM COMPRAS WHERE ID_FORNECEDOR = {id_fornecedor})",
                    f"DELETE FROM ITENS_COMPRA WHERE ID_PRODUTO IN "
                    f"(SELECT ID_PRODUTO FROM PRODUTOS WHERE ID_FORNECEDOR = {id_fornecedor})",
                    f"DELETE FROM COMPRAS WHERE ID_FORNECEDOR = {id_fornecedor}",
                    f"DELETE FROM PRODUTOS WHERE ID_FORNECEDOR = {id_fornecedor}",
                ]

            comandos.append(f"DELETE FROM FORNECEDORES WHERE ID_FORNECEDOR = {id_fornecedor}")
            # write_many executa tudo numa transação: ou apaga tudo, ou não apaga nada
            oracle.write_many(comandos)

        print("\nFornecedor removido com sucesso:")
        print(fornecedor.to_string())
        return True

    # ------------------------------------------------------------------
    # Funções de apoio
    # ------------------------------------------------------------------
    def existe_cnpj(self, oracle: OracleQueries, cnpj: str) -> bool:
        return self._contar(oracle, "FORNECEDORES", f"CNPJ = '{cnpj}'") > 0

    def _ler_cnpj(self) -> str:
        while True:
            cnpj = input("CNPJ (somente números): ").strip()
            cnpj = "".join(c for c in cnpj if c.isdigit())
            if len(cnpj) == 14:
                return cnpj
            print("O CNPJ deve ter 14 dígitos.")

    def _contar(self, oracle: OracleQueries, tabela: str, condicao: str) -> int:
        resultado = oracle.query(f"SELECT COUNT(1) AS TOTAL FROM {tabela} WHERE {condicao}")
        return int(resultado[0]["total"])

    def _buscar(self, oracle: OracleQueries, condicao: str) -> Fornecedor:
        linhas = oracle.query("SELECT ID_FORNECEDOR, RAZAO_SOCIAL, CNPJ, TELEFONE, EMAIL "
                              f"FROM FORNECEDORES WHERE {condicao}")
        if not linhas:
            return None
        f = linhas[0]
        return Fornecedor(f["id_fornecedor"], f["razao_social"], f["cnpj"], f["telefone"], f["email"])
