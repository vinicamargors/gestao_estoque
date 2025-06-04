import sqlite3
from app.models.Usuario import Usuario
from app.repositories.interfaces.IUsuarioRepository import IUsuarioRepository
import json

class UsuarioRepository(IUsuarioRepository):
    def __init__(self, db_path="estoque.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def adicionar(self, usuario):
        with self.conn:
            self.conn.execute("""
                INSERT INTO usuarios (id, nome, email, senha, cargo, permissoes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                usuario.id, usuario.nome, usuario.email, usuario.senha, usuario.cargo, json.dumps(usuario.permissoes)
            ))

    def buscar_por_email(self, email):
        cur = self.conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        row = cur.fetchone()
        if row:
            permissoes = json.loads(row["permissoes"])
            return Usuario(row["id"], row["nome"], row["email"], row["senha"], row["cargo"], permissoes)
        return None

    def listar_todos(self):
        cur = self.conn.execute("SELECT * FROM usuarios")
        usuarios = []
        for row in cur.fetchall():
            permissoes = json.loads(row["permissoes"])
            usuarios.append(Usuario(row["id"], row["nome"], row["email"], row["senha"], row["cargo"], permissoes))
        return usuarios
