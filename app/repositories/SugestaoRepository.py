import sqlite3
from app.models.Sugestao import Sugestao
from app.repositories.interfaces.ISugestaoRepository import ISugestaoRepository

class SugestaoRepository(ISugestaoRepository):
    def __init__(self, db_path="estoque.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def salvar(self, sugestao):
        with self.conn:
            self.conn.execute("""
                INSERT INTO sugestoes (produto_id, quantidade_sugerida, preco_sugerido, margem_usada)
                VALUES (?, ?, ?, ?)
            """, (
                sugestao.produto_id,
                sugestao.quantidade_sugerida,
                sugestao.preco_sugerido,
                sugestao.margem_usada
            ))

    def listar_por_produto(self, produto_id):
        cur = self.conn.execute("SELECT * FROM sugestoes WHERE produto_id = ?", (produto_id,))
        return [Sugestao(**row) for row in cur.fetchall()]
