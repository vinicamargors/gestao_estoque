import sqlite3
from app.models.Produto import Produto
from app.repositories.interfaces.IProdutoRepository import IProdutoRepository

class ProdutoRepository(IProdutoRepository):
    def __init__(self, db_path="estoque.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def adicionar(self, produto):
        with self.conn:
            self.conn.execute("""
                INSERT INTO produtos (id, nome, descricao, quantidade, preco_unitario, categoria, data_entrada, data_saida)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                produto.id, produto.nome, produto.descricao,
                produto.quantidade, produto.preco_unitario,
                produto.categoria, produto.data_entrada, produto.data_saida
            ))

    def remover(self, id_produto):
        with self.conn:
            self.conn.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))

    def atualizar(self, produto):
        with self.conn:
            self.conn.execute("""
                UPDATE produtos
                SET nome=?, descricao=?, quantidade=?, preco_unitario=?, categoria=?, data_entrada=?, data_saida=?
                WHERE id=?
            """, (
                produto.nome, produto.descricao, produto.quantidade,
                produto.preco_unitario, produto.categoria,
                produto.data_entrada, produto.data_saida, produto.id
            ))

    def buscar_por_id(self, id_produto):
        cur = self.conn.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
        row = cur.fetchone()
        return Produto(**row) if row else None

    def listar_todos(self):
        cur = self.conn.execute("SELECT * FROM produtos")
        return [Produto(**row) for row in cur.fetchall()]