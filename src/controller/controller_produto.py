from conexion.oracle_queries import OracleQueries, escapar
from controller.entrada import ler_texto, ler_inteiro, ler_decimal, confirmar
from model.fornecedor import Fornecedor
from model.produto import Produto


class Controller_Produto:

    # ------------------------------------------------------------------
    # INSERIR (edital 6.b)
    # ------------------------------------------------------------------
    def inserir_produto(self) -> Produto:
        print("\n--- Novo produto ---")
        with OracleQueries() as oracle:
            # Todo produto pertence a um fornecedor: mostra a lista para o usuário escolher
            self._listar_fornecedores(oracle)
            id_fornecedor = ler_inteiro("Código do fornecedor deste produto", minimo=1)
            if not self._existe(oracle, "FORNECEDORES", f"ID_FORNECEDOR = {id_fornecedor}"):
                print(f"O fornecedor de código {id_fornecedor} não existe. Cadastre-o primeiro.")
                return None

            nome = ler_texto("Nome do produto", tamanho_max=100)
            categoria = ler_texto("Categoria", tamanho_max=50)
            unidade = ler_texto("Unidade de medida (ex.: UN, KG, CX)", tamanho_max=10).upper()
            preco_custo = ler_decimal("Preço de custo (R$)")
            qtd_estoque = ler_inteiro("Quantidade em estoque", minimo=0, padrao=0)
            estoque_minimo = ler_inteiro("Estoque mínimo", minimo=0)

            # Monta o INSERT concatenando os valores digitados (sem ORM, conforme o edital)
            sql = ("INSERT INTO PRODUTOS (ID_PRODUTO, NOME, CATEGORIA, UNIDADE_MEDIDA, PRECO_CUSTO, "
                   "QTD_ESTOQUE, ESTOQUE_MINIMO, ID_FORNECEDOR) "
                   "VALUES (PRODUTOS_ID_SEQ.NEXTVAL, "
                   f"'{escapar(nome)}', '{escapar(categoria)}', '{escapar(unidade)}', "
                   f"{preco_custo}, {qtd_estoque}, {estoque_minimo}, {id_fornecedor})")
            oracle.write(sql)

            # CURRVAL devolve o último código gerado pela sequence nesta mesma conexão
            id_produto = oracle.query("SELECT PRODUTOS_ID_SEQ.CURRVAL AS ID FROM DUAL")[0]["id"]
            produto = self._buscar(oracle, id_produto)

        print("\nProduto cadastrado com sucesso:")
        print(produto.to_string())
        return produto

    # ------------------------------------------------------------------
    # ATUALIZAR (edital 6.d)
    # ------------------------------------------------------------------
    def atualizar_produto(self) -> Produto:
        with OracleQueries() as oracle:
            id_produto = ler_inteiro("\nCódigo do produto que deseja alterar", minimo=1)
            produto = self._buscar(oracle, id_produto)
            if produto is None:
                print(f"O produto de código {id_produto} não existe.")
                return None

            print("\nDados atuais:")
            print(produto.to_string())
            print("\nDigite os novos valores (ENTER mantém o valor atual):")

            nome = ler_texto("Nome do produto", tamanho_max=100, atual=produto.get_nome())
            categoria = ler_texto("Categoria", tamanho_max=50, atual=produto.get_categoria())
            unidade = ler_texto("Unidade de medida", tamanho_max=10,
                                atual=produto.get_unidade_medida()).upper()
            preco_custo = ler_decimal("Preço de custo (R$)", atual=produto.get_preco_custo())
            qtd_estoque = ler_inteiro("Quantidade em estoque", minimo=0, atual=produto.get_qtd_estoque())
            estoque_minimo = ler_inteiro("Estoque mínimo", minimo=0, atual=produto.get_estoque_minimo())

            # Só permite trocar o fornecedor se o produto ainda não aparece em nenhuma compra,
            # porque cada compra só pode ter produtos do fornecedor dela
            id_fornecedor = produto.get_fornecedor().get_id_fornecedor()
            if self._existe(oracle, "ITENS_COMPRA", f"ID_PRODUTO = {id_produto}"):
                print("(O fornecedor não pode ser alterado: este produto já aparece em compras.)")
            else:
                novo = ler_inteiro("Código do fornecedor", minimo=1, atual=id_fornecedor)
                if novo != id_fornecedor and not self._existe(oracle, "FORNECEDORES", f"ID_FORNECEDOR = {novo}"):
                    print(f"O fornecedor {novo} não existe. O fornecedor atual foi mantido.")
                else:
                    id_fornecedor = novo

            sql = (f"UPDATE PRODUTOS "
                   f"SET NOME = '{escapar(nome)}', "
                   f"CATEGORIA = '{escapar(categoria)}', "
                   f"UNIDADE_MEDIDA = '{escapar(unidade)}', "
                   f"PRECO_CUSTO = {preco_custo}, "
                   f"QTD_ESTOQUE = {qtd_estoque}, "
                   f"ESTOQUE_MINIMO = {estoque_minimo}, "
                   f"ID_FORNECEDOR = {id_fornecedor} "
                   f"WHERE ID_PRODUTO = {id_produto}")
            oracle.write(sql)

            produto = self._buscar(oracle, id_produto)

        print("\nProduto atualizado:")
        print(produto.to_string())
        return produto

    # ------------------------------------------------------------------
    # REMOVER (edital 6.c)
    # ------------------------------------------------------------------
    def excluir_produto(self) -> bool:
        with OracleQueries() as oracle:
            id_produto = ler_inteiro("\nCódigo do produto que deseja remover", minimo=1)
            produto = self._buscar(oracle, id_produto)
            if produto is None:
                print(f"O produto de código {id_produto} não existe.")
                return False

            print(produto.to_string())
            if not confirmar("Deseja realmente remover este produto?"):
                print("Remoção cancelada.")
                return "cancelado"   # volta ao menu principal (edital 6.c.5)

            comandos = []

            # (6.c.5.i) Verifica se o produto é chave estrangeira em ITENS_COMPRA
            qtd_itens = int(oracle.query("SELECT COUNT(1) AS TOTAL FROM ITENS_COMPRA "
                                         f"WHERE ID_PRODUTO = {id_produto}")[0]["total"])
            if qtd_itens > 0:
                print(f"\nAtenção: este produto aparece em {qtd_itens} item(ns) de compra.")
                if not confirmar("Deseja remover também esses itens de compra?"):
                    print("O produto não pode ser removido enquanto aparecer em compras.")
                    return False
                comandos.append(f"DELETE FROM ITENS_COMPRA WHERE ID_PRODUTO = {id_produto}")

            comandos.append(f"DELETE FROM PRODUTOS WHERE ID_PRODUTO = {id_produto}")
            # write_many executa tudo numa transação: ou apaga tudo, ou não apaga nada
            oracle.write_many(comandos)

        print("\nProduto removido com sucesso:")
        print(produto.to_string())
        return True

    # ------------------------------------------------------------------
    # Funções de apoio
    # ------------------------------------------------------------------
    def _existe(self, oracle: OracleQueries, tabela: str, condicao: str) -> bool:
        resultado = oracle.query(f"SELECT COUNT(1) AS TOTAL FROM {tabela} WHERE {condicao}")
        return int(resultado[0]["total"]) > 0

    def _listar_fornecedores(self, oracle: OracleQueries):
        print("\nFornecedores cadastrados:")
        for f in oracle.query("SELECT ID_FORNECEDOR, RAZAO_SOCIAL FROM FORNECEDORES ORDER BY ID_FORNECEDOR"):
            print(f"  {f['id_fornecedor']} - {f['razao_social']}")

    def _buscar(self, oracle: OracleQueries, id_produto: int) -> Produto:
        linhas = oracle.query(
            "SELECT PRO.ID_PRODUTO, PRO.NOME, PRO.CATEGORIA, PRO.UNIDADE_MEDIDA, PRO.PRECO_CUSTO, "
            "PRO.QTD_ESTOQUE, PRO.ESTOQUE_MINIMO, FORN.ID_FORNECEDOR, FORN.RAZAO_SOCIAL, "
            "FORN.CNPJ, FORN.TELEFONE, FORN.EMAIL "
            "FROM PRODUTOS PRO "
            "INNER JOIN FORNECEDORES FORN ON PRO.ID_FORNECEDOR = FORN.ID_FORNECEDOR "
            f"WHERE PRO.ID_PRODUTO = {id_produto}")
        if not linhas:
            return None
        p = linhas[0]
        fornecedor = Fornecedor(p["id_fornecedor"], p["razao_social"], p["cnpj"], p["telefone"], p["email"])
        return Produto(p["id_produto"], p["nome"], p["categoria"], p["unidade_medida"],
                       float(p["preco_custo"]), int(p["qtd_estoque"]), int(p["estoque_minimo"]), fornecedor)
