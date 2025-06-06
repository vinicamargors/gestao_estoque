from datetime import datetime

class Venda:
    def __init__(self, id, produto_id, quantidade, preco_total, data_venda=None):
        self.id = id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_total = preco_total
        self.data_venda = data_venda or datetime.today()

    def calcular_total(self, preco_unitario):
        self.preco_total = round(preco_unitario * self.quantidade, 2)

    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "preco_total": self.preco_total,
            "data_venda": self.data_venda
        }
