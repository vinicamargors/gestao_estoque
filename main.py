from login import abrir_login
from db import conectar_banco, criar_tabelas

conn = conectar_banco()
criar_tabelas(conn)
conn.close()


if __name__ == "__main__":
    abrir_login()
