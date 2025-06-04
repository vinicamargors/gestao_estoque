class Sugestao:
    def __init__(self, produto_id, quantidade_sugerida, preco_sugerido, margem_usada):
        self.produto_id = produto_id
        self.quantidade_sugerida = quantidade_sugerida
        self.preco_sugerido = preco_sugerido
        self.margem_usada = margem_usada

    def to_dict(self):
        return {
            "produto_id": self.produto_id,
            "quantidade_sugerida": self.quantidade_sugerida,
            "preco_sugerido": self.preco_sugerido,
            "margem_usada": self.margem_usada
        }