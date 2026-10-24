from model.fornecedor import Fornecedor


class Produto:
    """Representa uma linha da tabela PRODUTOS. Todo produto pertence a um fornecedor."""

    def __init__(self, id_produto: int = None, nome: str = None, categoria: str = None,
                 unidade_medida: str = None, preco_custo: float = None, qtd_estoque: int = 0,
                 estoque_minimo: int = 0, fornecedor: Fornecedor = None):
        self.set_id_produto(id_produto)
        self.set_nome(nome)
        self.set_categoria(categoria)
        self.set_unidade_medida(unidade_medida)
        self.set_preco_custo(preco_custo)
        self.set_qtd_estoque(qtd_estoque)
        self.set_estoque_minimo(estoque_minimo)
        self.set_fornecedor(fornecedor)

    def set_id_produto(self, id_produto: int):
        self.id_produto = id_produto

    def set_nome(self, nome: str):
        self.nome = nome

    def set_categoria(self, categoria: str):
        self.categoria = categoria

    def set_unidade_medida(self, unidade_medida: str):
        self.unidade_medida = unidade_medida

    def set_preco_custo(self, preco_custo: float):
        self.preco_custo = preco_custo

    def set_qtd_estoque(self, qtd_estoque: int):
        self.qtd_estoque = qtd_estoque

    def set_estoque_minimo(self, estoque_minimo: int):
        self.estoque_minimo = estoque_minimo

    def set_fornecedor(self, fornecedor: Fornecedor):
        self.fornecedor = fornecedor

    def get_id_produto(self) -> int:
        return self.id_produto

    def get_nome(self) -> str:
        return self.nome

    def get_categoria(self) -> str:
        return self.categoria

    def get_unidade_medida(self) -> str:
        return self.unidade_medida

    def get_preco_custo(self) -> float:
        return self.preco_custo

    def get_qtd_estoque(self) -> int:
        return self.qtd_estoque

    def get_estoque_minimo(self) -> int:
        return self.estoque_minimo

    def get_fornecedor(self) -> Fornecedor:
        return self.fornecedor

    def estoque_baixo(self) -> bool:
        return self.get_qtd_estoque() < self.get_estoque_minimo()

    def to_string(self) -> str:
        fornecedor = self.get_fornecedor().get_razao_social() if self.get_fornecedor() else "-"
        aviso = "  (ESTOQUE BAIXO)" if self.estoque_baixo() else ""
        return (f"Código: {self.get_id_produto()} | Produto: {self.get_nome()} | "
                f"Categoria: {self.get_categoria()} | Unidade: {self.get_unidade_medida()} | "
                f"Preço de custo: R$ {self.get_preco_custo():.2f} | "
                f"Estoque: {self.get_qtd_estoque()} (mínimo {self.get_estoque_minimo()}) | "
                f"Fornecedor: {fornecedor}{aviso}")
