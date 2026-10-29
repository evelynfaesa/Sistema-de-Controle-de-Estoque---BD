import os
from datetime import date, datetime

from conexion.oracle_queries import OracleQueries

# Pasta onde ficam os arquivos .sql dos relatórios (src/sql)
PASTA_SQL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql")


class Relatorio:
    """Executa as consultas da pasta src/sql e mostra o resultado em forma de tabela."""

    def __init__(self):
        # Lê o texto de cada consulta uma única vez, quando o objeto é criado
        self.query_quantidade_por_produto = self._ler_sql("relatorio_quantidade_por_produto.sql")
        self.query_itens_compra = self._ler_sql("relatorio_itens_compra.sql")
        self.query_estoque_baixo = self._ler_sql("relatorio_estoque_baixo.sql")
        self.query_fornecedores = self._ler_sql("relatorio_fornecedores.sql")
        self.query_produtos = self._ler_sql("relatorio_produtos.sql")
        self.query_compras = self._ler_sql("relatorio_compras.sql")

    # ------------------------------------------------------------------
    # Relatórios do menu "Relatórios"
    # ------------------------------------------------------------------
    def get_relatorio_quantidade_por_produto(self):
        """Relatório 1 - agrupamento (edital 6.a.1.i)."""
        self._executar("QUANTIDADE COMPRADA POR PRODUTO", self.query_quantidade_por_produto)

    def get_relatorio_itens_compra(self):
        """Relatório 2 - junção de tabelas (edital 6.a.1.ii)."""
        self._executar("ITENS DE COMPRA", self.query_itens_compra)

    def get_relatorio_estoque_baixo(self):
        """Relatório 3 - produtos abaixo do estoque mínimo."""
        self._executar("PRODUTOS COM ESTOQUE BAIXO", self.query_estoque_baixo,
                       mensagem_vazio="Nenhum produto está abaixo do estoque mínimo.")

    # ------------------------------------------------------------------
    # Listagens usadas antes de remover/atualizar (edital 6.c.3 e 6.d.3)
    # ------------------------------------------------------------------
    def get_relatorio_fornecedores(self):
        self._executar("FORNECEDORES", self.query_fornecedores)

    def get_relatorio_produtos(self):
        self._executar("PRODUTOS", self.query_produtos)

    def get_relatorio_compras(self):
        self._executar("COMPRAS", self.query_compras)

    # ------------------------------------------------------------------
    # Funções internas
    # ------------------------------------------------------------------
    def _ler_sql(self, nome_arquivo: str) -> str:
        with open(os.path.join(PASTA_SQL, nome_arquivo), encoding="utf-8") as arquivo:
            return arquivo.read()

    def _executar(self, titulo: str, sql: str, mensagem_vazio: str = "Nenhum registro encontrado."):
        """Abre a conexão, executa a consulta, mostra a tabela e fecha a conexão."""
        try:
            with OracleQueries() as oracle:
                linhas = oracle.query(sql)
        except Exception as erro:
            print(f"\nNão foi possível gerar o relatório: {erro}")
            return

        print(f"\n===== {titulo} =====")
        if not linhas:
            print(mensagem_vazio)
            return
        print(self._formatar_tabela(linhas))
        print(f"\nTotal de registros: {len(linhas)}")

    def _formatar_valor(self, valor) -> str:
        if valor is None:
            return "-"
        if isinstance(valor, (datetime, date)):
            return valor.strftime("%d/%m/%Y")
        if isinstance(valor, float):
            # 1234.5 -> "1.234,50" (padrão brasileiro)
            return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return str(valor)

    def _formatar_tabela(self, linhas: list) -> str:
        """Monta uma tabela de texto alinhada a partir da lista de dicionários do OracleQueries."""
        colunas = list(linhas[0].keys())
        titulos = [c.replace("_", " ").upper() for c in colunas]
        dados = [[self._formatar_valor(linha[c]) for c in colunas] for linha in linhas]

        larguras = [max(len(titulos[i]), *(len(d[i]) for d in dados)) for i in range(len(colunas))]

        def montar(valores):
            return " | ".join(v.ljust(larguras[i]) for i, v in enumerate(valores))

        separador = "-+-".join("-" * l for l in larguras)
        return "\n".join([montar(titulos), separador] + [montar(d) for d in dados])
