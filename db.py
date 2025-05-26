import sqlite3

def conectar_banco():
    conn = sqlite3.connect('estoque.db')
    return conn

def criar_tabelas(conn):
    cursor = conn.cursor()

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        )
    ''')

    conn.commit()
