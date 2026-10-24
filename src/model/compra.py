from datetime import date

from model.fornecedor import Fornecedor


class Compra:
    """Representa uma linha da tabela COMPRAS (o "cabeçalho" da compra, como uma nota fiscal)."""

    def __init__(self, id_compra: int = None, data_compra: date = None, fornecedor: Fornecedor = None):
        self.set_id_compra(id_compra)
        self.set_data_compra(data_compra)
        self.set_fornecedor(fornecedor)

    def set_id_compra(self, id_compra: int):
        self.id_compra = id_compra

    def set_data_compra(self, data_compra: date):
        self.data_compra = data_compra

    def set_fornecedor(self, fornecedor: Fornecedor):
        self.fornecedor = fornecedor

    def get_id_compra(self) -> int:
        return self.id_compra

    def get_data_compra(self) -> date:
        return self.data_compra

    def get_fornecedor(self) -> Fornecedor:
        return self.fornecedor

    def to_string(self) -> str:
        data = self.get_data_compra().strftime("%d/%m/%Y") if self.get_data_compra() else "-"
        fornecedor = self.get_fornecedor().get_razao_social() if self.get_fornecedor() else "-"
        return f"Compra: {self.get_id_compra()} | Data: {data} | Fornecedor: {fornecedor}"
