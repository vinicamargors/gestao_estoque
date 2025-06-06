from datetime import datetime


class Produto:
    def __init__(
        self,
        id,
        nome,
        descricao,
        quantidade,
        preco_unitario,
        categoria,
        data_entrada=None,
        data_saida=None,
    ):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.categoria = categoria
        self.data_entrada = data_entrada or datetime.today()
        self.data_saida = data_saida

    def atualizar_quantidade(self, nova_qtd):
        self.quantidade = nova_qtd

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "categoria": self.categoria,
            "data_entrada": self.data_entrada,
            "data_saida": self.data_saida,
        }
