"""
principal.py - Script principal: une entrada (telas), controladoras e relatórios.

Execução (a partir da raiz do projeto):  python3 src/principal.py

Variáveis de ambiente: ORA_USER, ORA_PASSWORD, ORA_DSN (ex.: localhost:1521/XEPDB1)
"""
import oracledb

import entrada
from conexao import Conexao
from controller.controller_compra import ControllerCompra
from controller.controller_fornecedor import ControllerFornecedor
from controller.controller_item_compra import ControllerItemCompra
from controller.controller_produto import ControllerProduto
from model.item_compra import ItemCompra
from reports.relatorios import Relatorios

CABECALHOS = {
    "1": ["ID", "RAZÃO SOCIAL"],
    "2": ["ID", "NOME"],
    "3": ["ID", "DATA", "FORNECEDOR"],
    "4": ["ID COMPRA", "ID PRODUTO", "PRODUTO", "QTD"],
}
TABELAS = [("FORNECEDORES", "fornecedores"), ("PRODUTOS", "produtos"),
           ("COMPRAS", "compras"), ("ITENS DE COMPRA", "itens_compra")]


def contar(conexao: Conexao, tabela: str) -> int:
    return conexao.valor("select count(1) total_" + tabela + " from " + tabela)


# ------------------------------------------------------------------ montagem dos objetos
def mostrar_fornecedores(ctrl: dict) -> bool:
    fornecedores = ctrl["1"].listar()
    if not fornecedores:
        print("Cadastre um fornecedor antes.")
        return False
    entrada.imprimir_tabela(CABECALHOS["1"], fornecedores)
    print()
    return True


def dados_produto(ctrl: dict, atual=None):
    """Lê o produto e vincula o fornecedor completo (associação)."""
    if not mostrar_fornecedores(ctrl):
        return None
    produto = entrada.ler_dados_produto(atual)
    fornecedor = ctrl["1"].buscar(produto.get_fornecedor().get_id_fornecedor())
    if fornecedor is None:
        print("Fornecedor não encontrado.")
        return None
    produto.set_fornecedor(fornecedor)
    return produto


def dados_compra(ctrl: dict, atual=None):
    if not mostrar_fornecedores(ctrl):
        return None
    compra = entrada.ler_dados_compra(atual)
    fornecedor = ctrl["1"].buscar(compra.get_fornecedor().get_id_fornecedor())
    if fornecedor is None:
        print("Fornecedor não encontrado.")
        return None
    compra.set_fornecedor(fornecedor)
    return compra


def dados_item_novo(ctrl: dict):
    """Escolhe a compra, mostra só os produtos do fornecedor dela e lê qtd/preço."""
    compras = ctrl["3"].listar()
    if not compras:
        print("Cadastre uma compra antes.")
        return None
    entrada.imprimir_tabela(CABECALHOS["3"], compras)
    id_compra = entrada.ler_inteiro("\nInforme o ID da compra: ")
    if id_compra is None:
        return None
    compra = ctrl["3"].buscar(id_compra)
    if compra is None:
        print("Compra não encontrada.")
        return None

    produtos = ctrl["2"].listar_por_fornecedor(compra.get_fornecedor().get_id_fornecedor())
    if not produtos:
        print("Este fornecedor não possui produtos cadastrados.")
        return None
    print("\nProdutos do fornecedor desta compra:")
    entrada.imprimir_tabela(CABECALHOS["2"], produtos)
    id_produto = entrada.ler_inteiro("\nInforme o ID do produto: ")
    if id_produto is None:
        return None
    produto = ctrl["2"].buscar(id_produto)
    if produto is None:
        print("Produto não encontrado.")
        return None

    qtd, preco = entrada.ler_quantidade_preco()
    return ItemCompra(compra, produto, qtd, preco)


def pedir_chave(op: str, acao: str):
    """Retorna a chave primária como tupla: (id,) ou (id_compra, id_produto)."""
    if op == "4":
        id_compra = entrada.ler_inteiro("\nInforme o ID da COMPRA do item a " + acao + ": ")
        if id_compra is None:
            return None
        id_produto = entrada.ler_inteiro("Informe o ID do PRODUTO do item: ")
        if id_produto is None:
            return None
        return (id_compra, id_produto)
    id_reg = entrada.ler_inteiro("\nInforme o ID a " + acao + ": ")
    return None if id_reg is None else (id_reg,)


# ------------------------------------------------------------------ fluxos
def fluxo_relatorios(relatorios: Relatorios):
    while True:
        op = entrada.menu_relatorios()
        if op == "0":
            return
        entrada.limpar()
        titulo, colunas, linhas = relatorios.executar(op)
        print("=== " + titulo + " ===\n")
        entrada.imprimir_tabela(colunas, linhas)
        entrada.pausar()


def fluxo_inserir(ctrl: dict):
    while True:
        op = entrada.menu_entidades()
        if op == "0":
            return
        while True:
            entrada.limpar()
            if op == "1":
                novo = entrada.ler_dados_fornecedor()
            elif op == "2":
                novo = dados_produto(ctrl)
            elif op == "3":
                novo = dados_compra(ctrl)
            else:
                novo = dados_item_novo(ctrl)
            if novo is not None and ctrl[op].inserir(novo):
                print("\nRegistro inserido com sucesso!")
                print(novo.to_string())
            if not entrada.confirmar("\nDeseja inserir mais algum registro?"):
                return


def fluxo_remover(ctrl: dict):
    while True:
        op = entrada.menu_entidades()
        if op == "0":
            return
        c = ctrl[op]
        while True:
            entrada.limpar()
            entrada.imprimir_tabela(CABECALHOS[op], c.listar())
            chave = pedir_chave(op, "remover")
            if chave is not None and c.existe(*chave):
                if entrada.confirmar("Deseja realmente remover este registro?"):
                    if c.tem_filhos(*chave):
                        print("Este registro possui registros dependentes em outras tabelas.")
                        if entrada.confirmar("Deseja remover também os registros filhos?"):
                            c.remover(*chave, apagar_filhos=True)
                            print("Registro e dependentes removidos.")
                        else:
                            print("Remoção cancelada.")
                    else:
                        c.remover(*chave)
                        print("Registro removido.")
                else:
                    return  # "Não" na confirmação volta ao menu principal
            elif chave is not None:
                print("Registro não encontrado.")
            if not entrada.confirmar("\nDeseja excluir mais algum registro?"):
                return


def fluxo_atualizar(ctrl: dict):
    while True:
        op = entrada.menu_entidades()
        if op == "0":
            return
        c = ctrl[op]
        while True:
            entrada.limpar()
            entrada.imprimir_tabela(CABECALHOS[op], c.listar())
            chave = pedir_chave(op, "atualizar")
            if chave is not None and c.existe(*chave):
                atual = c.buscar(*chave)
                if op == "1":
                    novo = entrada.ler_dados_fornecedor(atual)
                elif op == "2":
                    novo = dados_produto(ctrl, atual)
                elif op == "3":
                    novo = dados_compra(ctrl, atual)
                else:  # item: a PK não muda, só quantidade e preço
                    qtd, preco = entrada.ler_quantidade_preco(atual)
                    atual.set_quantidade(qtd)
                    atual.set_preco_unitario(preco)
                    novo = atual
                if novo is not None and c.atualizar(novo):
                    print("\nRegistro atualizado:")
                    print(c.buscar(*chave).to_string())
            elif chave is not None:
                print("Registro não encontrado.")
            if not entrada.confirmar("\nDeseja atualizar mais algum registro?"):
                return


# ------------------------------------------------------------------ main
def main():
    conexao = Conexao()
    ctrl = {"1": ControllerFornecedor(conexao), "2": ControllerProduto(conexao),
            "3": ControllerCompra(conexao), "4": ControllerItemCompra(conexao)}
    relatorios = Relatorios(conexao)

    try:
        entrada.splash_screen([(rotulo, contar(conexao, tabela)) for rotulo, tabela in TABELAS])
    except oracledb.Error as erro:
        print("Não foi possível consultar o banco de dados:\n", erro)
        print("\nConfira ORA_USER, ORA_PASSWORD, ORA_DSN e se o script "
              "sql/criar_tabelas.sql já foi executado.")
        return

    while True:
        op = entrada.menu_principal()
        if op == "0":
            print("Obrigado por utilizar o sistema. Até logo!")
            break
        try:
            if op == "1":
                fluxo_relatorios(relatorios)
            elif op == "2":
                fluxo_inserir(ctrl)
            elif op == "3":
                fluxo_remover(ctrl)
            elif op == "4":
                fluxo_atualizar(ctrl)
        except oracledb.Error as erro:  # ex.: violação de constraint, valor grande demais
            print("\nErro no banco de dados:", erro)
            entrada.pausar()


if __name__ == "__main__":
    main()
