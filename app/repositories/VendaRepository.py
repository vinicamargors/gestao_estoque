import sqlite3
from app.models.Venda import Venda
from app.repositories.interfaces.IVendaRepository import IVendaRepository

class VendaRepository(IVendaRepository):
    def __init__(self, db_path="estoque.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def registrar(self, venda):
        with self.conn:
            self.conn.execute("""
                INSERT INTO vendas (id, produto_id, quantidade, preco_total, data_venda)
                VALUES (?, ?, ?, ?, ?)
            """, (
                venda.id, venda.produto_id, venda.quantidade, venda.preco_total, venda.data_venda
            ))

    def listar_todas(self):
        cur = self.conn.execute("SELECT * FROM vendas")
        return [Venda(**row) for row in cur.fetchall()]

    def buscar_por_id(self, id_venda):
        cur = self.conn.execute("SELECT * FROM vendas WHERE id = ?", (id_venda,))
        row = cur.fetchone()
        return Venda(**row) if row else None

    def listar_por_produto(self, produto_id):
        cur = self.conn.execute("SELECT * FROM vendas WHERE produto_id = ?", (produto_id,))
        return [Venda(**row) for row in cur.fetchall()]

    def listar_por_periodo(self, data_inicio, data_fim):
        cur = self.conn.execute("""
            SELECT * FROM vendas WHERE data_venda BETWEEN ? AND ?
        """, (data_inicio, data_fim))
        return [Venda(**row) for row in cur.fetchall()]
