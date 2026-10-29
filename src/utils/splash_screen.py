from conexion.oracle_queries import OracleQueries
from utils import config


class SplashScreen:

    LARGURA = 50

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_fornecedores = config.QUERY_COUNT.format(tabela="fornecedores")
        self.qry_total_produtos = config.QUERY_COUNT.format(tabela="produtos")
        self.qry_total_compras = config.QUERY_COUNT.format(tabela="compras")
        self.qry_total_itens_compra = config.QUERY_COUNT.format(tabela="itens_compra")
        # Consultas de contagem de registros - fim

        # Nome(s) do(s) criador(es) e dados da disciplina
        self.created_by = config.NOMES_GRUPO
        self.professor = config.PROFESSOR
        self.disciplina = config.DISCIPLINA
        self.semestre = config.SEMESTRE

        # Guarda a mensagem do último erro de banco, para avisar o usuário
        self.erro = None

    def _get_total(self, query: str, coluna: str):
        """Abre uma conexão, executa a contagem e devolve o total (ou 'n/d' se falhar)."""
        try:
            with OracleQueries() as oracle:
                return oracle.query(query)[0][coluna]
        except Exception as erro:
            self.erro = str(erro)
            return "n/d"

    def get_total_fornecedores(self):
        return self._get_total(self.qry_total_fornecedores, "total_fornecedores")

    def get_total_produtos(self):
        return self._get_total(self.qry_total_produtos, "total_produtos")

    def get_total_compras(self):
        return self._get_total(self.qry_total_compras, "total_compras")

    def get_total_itens_compra(self):
        return self._get_total(self.qry_total_itens_compra, "total_itens_compra")

    # --------------------------------------------------------------------- tela
    def _linha(self, texto: str = "") -> str:
        return "# " + texto.ljust(self.LARGURA - 4) + " #"

    def _centralizada(self, texto: str) -> str:
        return "# " + texto.center(self.LARGURA - 4) + " #"

    def _linha_total(self, numero: int, rotulo: str, total) -> str:
        return self._linha(f"   {numero} - {rotulo}:".ljust(26) + str(total).rjust(10))

    def get_updated_screen(self) -> str:
        borda = "#" * self.LARGURA
        linhas = [
            borda,
            self._centralizada(config.NOME_SISTEMA),
            self._linha(),
            self._linha("TOTAL DE REGISTROS EXISTENTES"),
            self._linha_total(1, "FORNECEDORES", self.get_total_fornecedores()),
            self._linha_total(2, "PRODUTOS", self.get_total_produtos()),
            self._linha_total(3, "COMPRAS", self.get_total_compras()),
            self._linha_total(4, "ITENS DE COMPRA", self.get_total_itens_compra()),
            self._linha(),
        ]
        for i, nome in enumerate(self.created_by):
            prefixo = "CRIADO POR: " if i == 0 else " " * 12
            linhas.append(self._linha(prefixo + nome))
        linhas += [
            self._linha(),
            self._linha(f"DISCIPLINA: {self.disciplina}"),
            self._linha(" " * 12 + self.semestre),
            self._linha(f"PROFESSOR: {self.professor}"),
            borda,
        ]
        return "\n".join(linhas)

    def exibir(self):
        print(self.get_updated_screen())
        if self.erro:
            print(f"Aviso: não foi possível ler algum total do banco ({self.erro})")
