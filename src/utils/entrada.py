"""
entrada.py - Interação com o usuário (não acessa o banco de dados).

Responsável por: menus, nomes do grupo (splash screen) e leitura de dados.
"""
import os
from datetime import date, datetime

from model.compra import Compra
from model.fornecedor import Fornecedor
from model.produto import Produto

# ------------------------------------------------------------------ dados do grupo
NOME_SISTEMA = "SISTEMA DE CONTROLE DE ESTOQUE"
INTEGRANTES = ["Evelyn Constantino Bandeira", "Graciellen Reis Fagundes", "Micaellen Reis Fagundes",
DISCIPLINA = "BANCO DE DADOS"
SEMESTRE = "2026/2"
PROFESSOR = "HOWARD ROATTI"

# ------------------------------------------------------------------ menus

========== MENU PRINCIPAL ==========
 1 - Relatórios
 2 - Inserir registros
 3 - Remover registros
 4 - Atualizar registros
 0 - Sair
====================================="""


============= RELATÓRIOS ============
 1 - Total comprado por fornecedor (agrupamento)
 2 - Itens das compras (junção)
 3 - Produtos com estoque baixo
 0 - Voltar
====================================="""


============== ENTIDADES ============
 1 - Fornecedores
 2 - Produtos
 3 - Compras
 4 - Itens de compra
 0 - Voltar
====================================="""


# ------------------------------------------------------------------ telas
def limpar():
    os.system("clear")


def pausar():
    input("\nPressione ENTER para continuar...")


def imprimir_tabela(colunas, linhas):
    if not linhas:
        print("Nenhum registro encontrado.")
        return
    linhas = [["-" if v is None else v for v in l] for l in linhas]
    larguras = [max(len(str(c)), *(len(str(l[i])) for l in linhas))
                for i, c in enumerate(colunas)]
    print(" | ".join(str(c).ljust(larguras[i]) for i, c in enumerate(colunas)))
    print("-+-".join("-" * w for w in larguras))
    for l in linhas:
        print(" | ".join(str(v).ljust(larguras[i]) for i, v in enumerate(l)))


# ------------------------------------------------------------------ leitura de dados
def confirmar(pergunta: str) -> bool:
    return input(pergunta + " (S/N): ").strip().upper() == "S"


def ler_opcao(opcoes_validas) -> str:
    while True:
        op = input("Escolha uma opção: ").strip()
        if op in opcoes_validas:
            return op
        print("Opção inválida.")


def ler_inteiro(mensagem: str):
    """Para escolher um ID. Retorna None se o valor for inválido."""
    try:
        return int(input(mensagem).strip())
    except ValueError:
        print("Valor inválido, digite um número inteiro.")
        return None


def ler_texto(mensagem: str, atual: str = None, obrigatorio: bool = True,
              maximo: int = 100) -> str:
    """Na atualização (atual informado), ENTER mantém o valor atual."""
    while True:
        sufixo = " [" + str(atual) + "]" if atual else ""
        txt = input(mensagem + sufixo + ": ").strip()
        if txt == "" and atual:
            return atual
        if txt == "" and obrigatorio:
            print("Campo obrigatório.")
            continue
        if len(txt) > maximo:
            print("Máximo de " + str(maximo) + " caracteres.")
            continue
        return txt


def ler_numero(mensagem: str, tipo=int, atual=None, positivo: bool = False):
    """Lê número. positivo=True exige > 0; senão aceita >= 0. ENTER mantém o atual."""
    while True:
        sufixo = " [" + str(atual) + "]" if atual is not None else ""
        txt = input(mensagem + sufixo + ": ").strip().replace(",", ".")
        if txt == "" and atual is not None:
            return atual
        try:
            valor = tipo(txt)
        except ValueError:
            print("Valor inválido.")
            continue
        if positivo and valor <= 0:
            print("Informe um valor maior que zero.")
            continue
        if valor < 0:
            print("Informe um valor maior ou igual a zero.")
            continue
        return valor


def ler_cnpj(atual: str = None) -> str:
    """Aceita com ou sem pontuação; guarda só os 14 dígitos (CHAR(14))."""
    while True:
        sufixo = " [" + str(atual).strip() + "]" if atual else ""
        txt = input("CNPJ (14 dígitos)" + sufixo + ": ").strip()
        if txt == "" and atual:
            return str(atual).strip()
        digitos = "".join(c for c in txt if c.isdigit())
        if len(digitos) == 14:
            return digitos
        print("CNPJ inválido: informe 14 dígitos.")


def ler_data(mensagem: str, atual=None):
    """ENTER usa a data atual do registro (ou hoje, se for novo)."""
    padrao = atual if atual else date.today()
    while True:
        txt = input(mensagem + " [" + padrao.strftime("%d/%m/%Y") + "]: ").strip()
        if txt == "":
            return padrao
        try:
            return datetime.strptime(txt, "%d/%m/%Y").date()
        except ValueError:
            print("Data inválida. Use DD/MM/AAAA.")


def ler_dados_fornecedor(atual: Fornecedor = None) -> Fornecedor:
    razao = ler_texto("Razão social", atual.get_razao_social() if atual else None)
    cnpj = ler_cnpj(atual.get_cnpj() if atual else None)
    telefone = ler_texto("Telefone (opcional)", atual.get_telefone() if atual else None,
                         obrigatorio=False, maximo=15)
    email = ler_texto("E-mail (opcional)", atual.get_email() if atual else None,
                      obrigatorio=False, maximo=100)
    return Fornecedor(atual.get_id_fornecedor() if atual else None, razao, cnpj, telefone, email)


def ler_dados_produto(atual: Produto = None) -> Produto:
    """Retorna o Produto com um Fornecedor que contém só o ID informado;
    o principal.py busca o fornecedor completo no banco."""
    nome = ler_texto("Nome", atual.get_nome() if atual else None)
    categoria = ler_texto("Categoria", atual.get_categoria() if atual else None, maximo=50)
    unidade = ler_texto("Unidade de medida (ex.: UN, KG)",
                        atual.get_unidade_medida() if atual else None, maximo=10)
    preco = ler_numero("Preço de custo", float, atual.get_preco_custo() if atual else None,
                       positivo=True)
    qtd = ler_numero("Quantidade em estoque", int, atual.get_qtd_estoque() if atual else None)
    minimo = ler_numero("Estoque mínimo", int, atual.get_estoque_minimo() if atual else None)
    id_forn = ler_numero("ID do fornecedor", int,
                         atual.get_fornecedor().get_id_fornecedor() if atual else None,
                         positivo=True)
    return Produto(atual.get_id_produto() if atual else None, nome, categoria, unidade,
                   preco, qtd, minimo, Fornecedor(id_forn))


def ler_dados_compra(atual: Compra = None) -> Compra:
    """Retorna a Compra com um Fornecedor que contém só o ID informado."""
    data = ler_data("Data da compra (DD/MM/AAAA)", atual.get_data_compra() if atual else None)
    id_forn = ler_numero("ID do fornecedor", int,
                         atual.get_fornecedor().get_id_fornecedor() if atual else None,
                         positivo=True)
    return Compra(atual.get_id_compra() if atual else None, data, Fornecedor(id_forn))


def ler_quantidade_preco(atual=None):
    """Lê quantidade e preço unitário de um item. 'atual' é um ItemCompra (atualização)."""
    qtd = ler_numero("Quantidade", int, atual.get_quantidade() if atual else None, positivo=True)
    preco = ler_numero("Preço unitário", float,
                       atual.get_preco_unitario() if atual else None, positivo=True)
    return qtd, preco


# ------------------------------------------------------------------ menus (exibem e retornam a escolha)
def menu_principal() -> str:
    limpar()
    print(MENU_PRINCIPAL)
    return ler_opcao({"0", "1", "2", "3", "4"})


def menu_relatorios() -> str:
    limpar()
    print(MENU_RELATORIOS)
    return ler_opcao({"0", "1", "2", "3"})


def menu_entidades() -> str:
    limpar()
    print(MENU_ENTIDADES)
    return ler_opcao({"0", "1", "2", "3", "4"})


# ------------------------------------------------------------------ splash screen
def splash_screen(totais):
    """totais: lista de (rotulo, quantidade)."""
    limpar()
    largura = 48
    borda = "#" * largura

    def linha(txt=""):
        print("# " + txt.ljust(largura - 4) + " #")

    print(borda)
    linha(NOME_SISTEMA.center(largura - 4))
    linha()
    linha("TOTAL DE REGISTROS EXISTENTES")
    for i, (rotulo, qtd) in enumerate(totais, start=1):
        linha("  " + str(i) + " - " + rotulo + ": " + str(qtd))
    linha()
    linha("CRIADO POR:")
    for nome in INTEGRANTES:
        linha("  " + nome)
    linha()
    linha("DISCIPLINA: " + DISCIPLINA)
    linha("            " + SEMESTRE)
    linha("PROFESSOR: " + PROFESSOR)
    print(borda)
    pausar()
