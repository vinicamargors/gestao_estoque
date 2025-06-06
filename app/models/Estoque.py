from app.models.Produto import Produto

class Estoque:
    def __init__(self):
        self._produtos = []

    def adicionar_produto(self, produto: Produto):
        self._produtos.append(produto)

    def remover_produto(self, id_produto):
        self._produtos = [p for p in self._produtos if p.id != id_produto]

    def consultar_estoque(self):
        return self._produtos

    def buscar_por_id(self, id_produto):
        for produto in self._produtos:
            if produto.id == id_produto:
                return produto
        return None
