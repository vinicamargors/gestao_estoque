from app.repositories.interfaces.IEstoqueRepository import IEstoqueRepository
from app.models.Produto import Produto
import sqlite3

class EstoqueRepository(IEstoqueRepository):
    def __init__(self, db_path="estoque.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def carregar_estoque(self):
        cur = self.conn.execute("SELECT * FROM produtos")
        return [Produto(**row) for row in cur.fetchall()]

    def salvar_produto(self, produto):
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO produtos (id, nome, descricao, quantidade, preco_unitario, categoria, data_entrada, data_saida)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                produto.id, produto.nome, produto.descricao, produto.quantidade,
                produto.preco_unitario, produto.categoria, produto.data_entrada, produto.data_saida
            ))

    def deletar_produto(self, id_produto):
        with self.conn:
            self.conn.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
