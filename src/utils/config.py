
config.py
100%
"""Configurações gerais e menus do sistema."""
import os

# ----------------------------------------------------------------- identificação
NOME_SISTEMA = "SISTEMA DE CONTROLE DE ESTOQUE"
NOMES_GRUPO = [
    "EVELYN CONSTANTINO BANDEIRA",  
    "GRACIELLEN REIS FAGUNDES",
    "MICAELLEN REIS FAGUNDES",
]
DISCIPLINA = "BANCO DE DADOS"
SEMESTRE = "2026/2"
PROFESSOR = "HOWARD ROATTI"

TABELAS = {
    "FORNECEDORES": "fornecedores",
    "PRODUTOS": "produtos",
    "COMPRAS": "compras",
    "ITENS DE COMPRA": "itens_compra",
}

# ------------------------------------------------------------------------ menus
MENU_PRINCIPAL = [
    ("1", "Relatórios"),
    ("2", "Inserir Registros"),
    ("3", "Remover Registros"),
    ("4", "Atualizar Registros"),
    ("5", "Sair"),
]

MENU_RELATORIOS = [
    ("1", "Quantidade comprada por produto"),
    ("2", "Itens de compra (compra, fornecedor e produto)"),
    ("3", "Produtos com estoque baixo"),
    ("0", "Voltar ao menu principal"),
]

MENU_ENTIDADES = [
    ("1", "Fornecedores"),
    ("2", "Produtos"),
    ("3", "Compras"),
    ("4", "Itens de Compra"),
    ("0", "Voltar ao menu principal"),
]


# ------------------------------------------------------------ funções auxiliares
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def exibir_menu(titulo: str, opcoes: list):
    """Mostra um menu no console. 'opcoes' é uma lista de tuplas (código, descrição)."""
    largura = max(len(titulo), *(len(f"{c} - {d}") for c, d in opcoes)) + 4
    print("=" * largura)
    print(titulo.center(largura))
    print("=" * largura)
    for codigo, descricao in opcoes:
        print(f"  {codigo} - {descricao}")
    print("=" * largura)


def ler_opcao(opcoes: list) -> str:
    """Lê uma opção do menu e só devolve quando for uma das opções válidas."""
    validas = [codigo for codigo, _ in opcoes]
    while True:
        escolha = input("Escolha uma opção: ").strip()
        if escolha in validas:
            return escolha
        print(f"Opção inválida. Escolha entre: {', '.join(validas)}")


def pausar():
    input("\nPressione Enter para continuar...")
Exibindo config.py…
