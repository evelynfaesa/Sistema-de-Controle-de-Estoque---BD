class Fornecedor:
    """Representa uma linha da tabela FORNECEDORES."""

    def __init__(self, id_fornecedor: int = None, razao_social: str = None,
                 cnpj: str = None, telefone: str = None, email: str = None):
        self.set_id_fornecedor(id_fornecedor)
        self.set_razao_social(razao_social)
        self.set_cnpj(cnpj)
        self.set_telefone(telefone)
        self.set_email(email)

    def set_id_fornecedor(self, id_fornecedor: int):
        self.id_fornecedor = id_fornecedor

    def set_razao_social(self, razao_social: str):
        self.razao_social = razao_social

    def set_cnpj(self, cnpj: str):
        self.cnpj = cnpj

    def set_telefone(self, telefone: str):
        self.telefone = telefone

    def set_email(self, email: str):
        self.email = email

    def get_id_fornecedor(self) -> int:
        return self.id_fornecedor

    def get_razao_social(self) -> str:
        return self.razao_social

    def get_cnpj(self) -> str:
        return self.cnpj

    def get_telefone(self) -> str:
        return self.telefone

    def get_email(self) -> str:
        return self.email

    def to_string(self) -> str:
        return (f"Código: {self.get_id_fornecedor()} | Razão Social: {self.get_razao_social()} | "
                f"CNPJ: {self.get_cnpj()} | Telefone: {self.get_telefone() or '-'} | "
                f"E-mail: {self.get_email() or '-'}")
