import os
import sys

from controller.controller_compra import Controller_Compra
from controller.controller_fornecedor import Controller_Fornecedor
from controller.controller_item_compra import Controller_Item_Compra
from controller.controller_produto import Controller_Produto
from reports.relatorios import Relatorio
from utils import config
from utils.entrada import confirmar
from utils.splash_screen import SplashScreen


def executar(acao):
    """Executa uma operação sem derrubar o programa se o banco devolver erro."""
    try:
        return acao()
    except Exception as erro:
        print(f"Erro ao executar a operação: {erro}")


def menu_relatorios():
    relatorio = Relatorio()
    acoes = {
        "1": relatorio.get_relatorio_quantidade_por_produto,
        "2": relatorio.get_relatorio_itens_compra,
        "3": relatorio.get_relatorio_estoque_baixo,
    }
    while True:
        config.limpar_tela()
        config.exibir_menu("RELATÓRIOS", config.MENU_RELATORIOS)
        opcao = config.ler_opcao(config.MENU_RELATORIOS)
        if opcao == "0":
            return
        executar(acoes[opcao])
        config.pausar()


def menu_entidades(titulo: str, acoes: dict, pergunta: str, listagens: dict = None):
    """Menu de entidades usado por inserir, remover e atualizar.

    Depois de cada operação pergunta se o usuário quer continuar: se sim, o menu de
    entidades é exibido de novo; se não, volta ao menu principal.
    'listagens' mostra os registros da tabela antes de remover/atualizar (edital 6.c.3 e 6.d.3).
    """
    while True:
        config.limpar_tela()
        config.exibir_menu(titulo, config.MENU_ENTIDADES)
        opcao = config.ler_opcao(config.MENU_ENTIDADES)
        if opcao == "0":
            return
        if listagens:
            executar(listagens[opcao])
        resultado = executar(acoes[opcao])
        # (6.c.5) Se o usuário desistiu da remoção, volta direto ao menu principal
        if resultado == "cancelado":
            return
        if not confirmar(pergunta):
            return


def listagens() -> dict:
    """Relatórios mostrados antes de remover/atualizar, para o usuário ver os códigos."""
    relatorio = Relatorio()
    return {
        "1": relatorio.get_relatorio_fornecedores,
        "2": relatorio.get_relatorio_produtos,
        "3": relatorio.get_relatorio_compras,
        "4": relatorio.get_relatorio_itens_compra,
    }


def inserir_registros():
    fornecedor, produto = Controller_Fornecedor(), Controller_Produto()
    compra, item = Controller_Compra(), Controller_Item_Compra()
    acoes = {
        "1": fornecedor.inserir_fornecedor,
        "2": produto.inserir_produto,
        "3": compra.inserir_compra,
        "4": item.inserir_item_compra,
    }
    menu_entidades("INSERIR REGISTROS", acoes, "Deseja inserir mais algum registro?")


def remover_registros():
    fornecedor, produto = Controller_Fornecedor(), Controller_Produto()
    compra, item = Controller_Compra(), Controller_Item_Compra()
    acoes = {
        "1": fornecedor.excluir_fornecedor,
        "2": produto.excluir_produto,
        "3": compra.excluir_compra,
        "4": item.excluir_item_compra,
    }
    menu_entidades("REMOVER REGISTROS", acoes, "Deseja remover mais algum registro?", listagens())


def atualizar_registros():
    fornecedor, produto = Controller_Fornecedor(), Controller_Produto()
    compra, item = Controller_Compra(), Controller_Item_Compra()
    acoes = {
        "1": fornecedor.atualizar_fornecedor,
        "2": produto.atualizar_produto,
        "3": compra.atualizar_compra,
        "4": item.atualizar_item_compra,
    }
    menu_entidades("ATUALIZAR REGISTROS", acoes, "Deseja atualizar mais algum registro?", listagens())


def run():
    if not os.getenv("ORACLE_USER") or not os.getenv("ORACLE_PASSWORD"):
        print("Defina as variáveis de ambiente antes de executar:")
        print("  export ORACLE_USER=seu_usuario")
        print("  export ORACLE_PASSWORD=sua_senha")
        print("  export ORACLE_DSN=host:porta/servico   (opcional; padrão: localhost:1521/XEPDB1)")
        sys.exit(1)

    config.limpar_tela()
    SplashScreen().exibir()
    config.pausar()

    while True:
        config.limpar_tela()
        config.exibir_menu("MENU PRINCIPAL", config.MENU_PRINCIPAL)
        opcao = config.ler_opcao(config.MENU_PRINCIPAL)

        if opcao == "1":
            menu_relatorios()
        elif opcao == "2":
            inserir_registros()
        elif opcao == "3":
            remover_registros()
        elif opcao == "4":
            atualizar_registros()
        elif opcao == "5":
            print("\nObrigado por utilizar o sistema. Até logo!")
            break


if __name__ == "__main__":
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma encerrado.")
