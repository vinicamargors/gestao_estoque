import sqlite3
import hashlib
from datetime import datetime, timedelta

# ---------- HASH DE SENHA ----------
def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# ---------- CONECTAR BANCO E CRIAR TABELAS ----------
def conectar_banco():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Cria tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT,
            fornecedor TEXT,
            data_entrada DATE NOT NULL,
            data_validade DATE NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_base REAL NOT NULL
        )
    ''')

    # Cria tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        )
    ''')

    conn.commit()
    return conn

# ---------- CRIAR NOVO USUÁRIO ----------
def criar_usuario(conn):
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")
    senha_hash = gerar_hash_senha(senha)

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
                       (nome, email, senha_hash))
        conn.commit()
        print("Usuário cadastrado com sucesso.")
    except sqlite3.IntegrityError:
        print("Erro: esse e-mail já está cadastrado.")

# ---------- LOGIN DE USUÁRIO ----------
def fazer_login(conn):
    email = input("Email: ")
    senha = input("Senha: ")
    senha_hash = gerar_hash_senha(senha)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha_hash = ?", (email, senha_hash))
    usuario = cursor.fetchone()

    if usuario:
        print(f"\nBem-vindo(a), {usuario[1]}!")
        return True
    else:
        print("Login inválido.")
        return False

# ---------- FUNÇÕES DE ESTOQUE (iguais às anteriores) ----------
def listar_todos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    for p in produtos:
        print(f"[{p[0]}] {p[1]} - Qtd: {p[6]} - R$ {p[7]:.2f} - Vence: {p[5]}")
    print()

def pesquisar_por_nome(conn):
    nome = input("Nome: ")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", ('%' + nome + '%',))
    for p in cursor.fetchall():
        print(f"[{p[0]}] {p[1]} - Qtd: {p[6]} - Vence: {p[5]}")

def pesquisar_por_data(conn):
    data = input("Data (YYYY-MM-DD): ")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE data_validade = ?", (data,))
    for p in cursor.fetchall():
        print(f"[{p[0]}] {p[1]} - Qtd: {p[6]}")

def calcular_desconto(preco, dias):
    if dias <= 2:
        return preco * 0.5
    elif dias <= 5:
        return preco * 0.7
    elif dias <= 10:
        return preco * 0.9
    return preco

def verificar_validade(conn):
    hoje = datetime.today().date()
    limite = hoje + timedelta(days=10)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE data_validade <= ?", (limite,))
    for p in cursor.fetchall():
        dias = (datetime.strptime(p[5], "%Y-%m-%d").date() - hoje).days
        preco = calcular_desconto(p[7], dias)
        print(f"[{p[0]}] {p[1]} - {dias} dias p/ vencer - Preço: R$ {preco:.2f}")

def inserir_produto(conn):
    nome = input("Nome: ")
    cat = input("Categoria: ")
    forn = input("Fornecedor: ")
    entrada = input("Data entrada (YYYY-MM-DD): ")
    validade = input("Validade (YYYY-MM-DD): ")
    qtd = int(input("Quantidade: "))
    preco = float(input("Preço base: "))

    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, categoria, fornecedor, data_entrada, data_validade, quantidade, preco_base) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (nome, cat, forn, entrada, validade, qtd, preco))
    conn.commit()
    print("Produto inserido.")

def editar_produto(conn):
    id = input("ID do produto: ")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
    p = cursor.fetchone()
    if not p:
        print("Produto não encontrado.")
        return

    nome = input(f"Nome ({p[1]}): ") or p[1]
    categoria = input(f"Categoria ({p[2]}): ") or p[2]
    fornecedor = input(f"Fornecedor ({p[3]}): ") or p[3]
    entrada = input(f"Data entrada ({p[4]}): ") or p[4]
    validade = input(f"Validade ({p[5]}): ") or p[5]
    quantidade = input(f"Quantidade ({p[6]}): ") or p[6]
    preco = input(f"Preço base ({p[7]}): ") or p[7]

    cursor.execute('''
        UPDATE produtos SET nome=?, categoria=?, fornecedor=?, data_entrada=?, data_validade=?, quantidade=?, preco_base=?
        WHERE id=?
    ''', (nome, categoria, fornecedor, entrada, validade, quantidade, preco, id))
    conn.commit()
    print("Produto atualizado.")

def excluir_produto(conn):
    id = input("ID para excluir: ")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    print("Produto excluído.")

# ---------- MENU DE ESTOQUE (após login) ----------
def menu_estoque(conn):
    while True:
        print("\n=== MENU ESTOQUE ===")
        print("1 - Listar tudo")
        print("  1.1 - Editar ou excluir produto")
        print("2 - Pesquisar por nome")
        print("3 - Pesquisar por data de vencimento")
        print("4 - Verificar validade e descontos")
        print("5 - Inserir novo produto")
        print("0 - Sair")
        op = input("Opção: ")

        if op == "1":
            listar_todos(conn)
        elif op == "1.1":
            sub = input("'e' editar / 'x' excluir: ")
            if sub == 'e':
                editar_produto(conn)
            elif sub == 'x':
                excluir_produto(conn)
        elif op == "2":
            pesquisar_por_nome(conn)
        elif op == "3":
            pesquisar_por_data(conn)
        elif op == "4":
            verificar_validade(conn)
        elif op == "5":
            inserir_produto(conn)
        elif op == "0":
            break
        else:
            print("Opção inválida.")

# ---------- MENU DE LOGIN ----------
def menu_login():
    conn = conectar_banco()
    while True:
        print("\n=== LOGIN SISTEMA DE ESTOQUE ===")
        print("1 - Login")
        print("2 - Criar novo usuário")
        print("0 - Sair")
        op = input("Opção: ")

        if op == "1":
            if fazer_login(conn):
                menu_estoque(conn)
        elif op == "2":
            criar_usuario(conn)
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
    conn.close()

# ---------- INICIAR ----------
menu_login()
