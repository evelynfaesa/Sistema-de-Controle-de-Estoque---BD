"""Funções de apoio para ler dados do teclado com validação.
Usadas pelos controllers para o programa não travar quando o usuário digita algo errado."""


def ler_texto(mensagem: str, obrigatorio: bool = True, tamanho_max: int = None, atual: str = None) -> str:
    """Lê um texto. Se 'atual' for informado (atualização), ENTER mantém o valor atual."""
    while True:
        sufixo = f" [atual: {atual}]" if atual is not None else ""
        valor = input(f"{mensagem}{sufixo}: ").strip()
        if valor == "" and atual is not None:
            return atual
        if valor == "" and not obrigatorio:
            return None
        if valor == "":
            print("Este campo é obrigatório.")
            continue
        if tamanho_max and len(valor) > tamanho_max:
            print(f"Máximo de {tamanho_max} caracteres.")
            continue
        return valor


def ler_inteiro(mensagem: str, minimo: int = None, atual: int = None, padrao: int = None) -> int:
    """Lê um número inteiro. ENTER mantém o valor atual (atualização) ou usa o padrão."""
    while True:
        sufixo = f" [atual: {atual}]" if atual is not None else (f" [padrão: {padrao}]" if padrao is not None else "")
        valor = input(f"{mensagem}{sufixo}: ").strip()
        if valor == "":
            if atual is not None:
                return atual
            if padrao is not None:
                return padrao
            print("Este campo é obrigatório.")
            continue
        if not valor.lstrip("-").isdigit():
            print("Digite apenas números inteiros.")
            continue
        numero = int(valor)
        if minimo is not None and numero < minimo:
            print(f"O valor deve ser maior ou igual a {minimo}.")
            continue
        return numero


def ler_decimal(mensagem: str, maior_que_zero: bool = True, atual: float = None) -> float:
    """Lê um número decimal, aceitando vírgula ou ponto (ex.: 22,90 ou 22.90)."""
    while True:
        sufixo = f" [atual: {atual:.2f}]" if atual is not None else ""
        valor = input(f"{mensagem}{sufixo}: ").strip().replace(",", ".")
        if valor == "" and atual is not None:
            return atual
        try:
            numero = round(float(valor), 2)
        except ValueError:
            print("Digite um número válido (ex.: 22,90).")
            continue
        if maior_que_zero and numero <= 0:
            print("O valor deve ser maior que zero.")
            continue
        return numero


def confirmar(mensagem: str) -> bool:
    """Pergunta Sim/Não e devolve True para Sim."""
    while True:
        resposta = input(f"{mensagem} [S/N]: ").strip().upper()
        if resposta in ("S", "SIM"):
            return True
        if resposta in ("N", "NAO", "NÃO"):
            return False
        print("Responda S (Sim) ou N (Não).")
