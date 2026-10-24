from model.compra import Compra
from model.produto import Produto


class ItemCompra:
    """Representa uma linha da tabela ITENS_COMPRA.
    A chave primária é composta: compra + produto."""

    def __init__(self, compra: Compra = None, produto: Produto = None,
                 quantidade: int = None, preco_unitario: float = None):
        self.set_compra(compra)
        self.set_produto(produto)
        self.set_quantidade(quantidade)
        self.set_preco_unitario(preco_unitario)

    def set_compra(self, compra: Compra):
        self.compra = compra

    def set_produto(self, produto: Produto):
        self.produto = produto

    def set_quantidade(self, quantidade: int):
        self.quantidade = quantidade

    def set_preco_unitario(self, preco_unitario: float):
        self.preco_unitario = preco_unitario

    def get_compra(self) -> Compra:
        return self.compra

    def get_produto(self) -> Produto:
        return self.produto

    def get_quantidade(self) -> int:
        return self.quantidade

    def get_preco_unitario(self) -> float:
        return self.preco_unitario

    def get_valor_total(self) -> float:
        return self.get_quantidade() * self.get_preco_unitario()

    def to_string(self) -> str:
        compra = self.get_compra().get_id_compra() if self.get_compra() else "-"
        produto = self.get_produto().get_nome() if self.get_produto() else "-"
        return (f"Compra: {compra} | Produto: {produto} | Quantidade: {self.get_quantidade()} | "
                f"Preço unitário: R$ {self.get_preco_unitario():.2f} | "
                f"Valor do item: R$ {self.get_valor_total():.2f}")
