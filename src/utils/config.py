import os

# =====================================================================
# Dados do sistema e do grupo (usados na splash screen)
# =====================================================================
NOME_SISTEMA = "SISTEMA DE CONTROLE DE ESTOQUE"
NOMES_GRUPO = [
    "Evelyn Constantino Bandeira",
    "Graciellen Reis Fagundes",
    "Micaellen Reis Fagundes",
]
DISCIPLINA = "Banco de Dados"
SEMESTRE = "2026/2"
PROFESSOR = "Prof. M.Sc. Howard Roatti"

# Contagem de registros exigida pelo edital (item 5.c)
QUERY_COUNT = "select count(1) as total_{tabela} from {tabela}"

# =====================================================================
# Menus: cada chave é a opção que o usuário digita
# =====================================================================
MENU_PRINCIPAL = {
    "1": "Relatórios",
    "2": "Inserir Registros",
    "3": "Remover Registros",
    "4": "Atualizar Registros",
    "5": "Sair",
}

MENU_RELATORIOS = {
    "1": "Quantidade Comprada por Produto (agrupamento)",
    "2": "Itens de Compra (junção de tabelas)",
    "3": "Produtos com Estoque Baixo",
    "0": "Voltar ao Menu Principal",
}

MENU_ENTIDADES = {
    "1": "Fornecedores",
    "2": "Produtos",
    "3": "Compras",
    "4": "Itens de Compra",
    "0": "Voltar ao Menu Principal",
}


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def exibir_menu(titulo: str, menu: dict):
    print("=" * 50)
    print(titulo.center(50))
    print("=" * 50)
    for opcao, descricao in menu.items():
        print(f"  {opcao} - {descricao}")
    print("=" * 50)


def ler_opcao(menu: dict) -> str:
    """Repete a pergunta até o usuário digitar uma das opções do menu."""
    opcoes = list(menu.keys())
    while True:
        opcao = input(f"Escolha uma opção [{', '.join(sorted(opcoes))}]: ").strip()
        if opcao in opcoes:
            return opcao
        print("Opção inválida. Tente novamente.")


def pausar():
    input("\nPressione ENTER para continuar...")
