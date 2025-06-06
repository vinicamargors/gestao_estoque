from app.repositories.interfaces.IProdutoRepository import IProdutoRepository
from app.models.Produto import Produto

class ProdutoService:
    def __init__(self, repo: IProdutoRepository):
        self.repo = repo

    def criar_produto(self, id, nome, descricao, quantidade, preco, categoria):
        produto = Produto(id, nome, descricao, quantidade, preco, categoria)
        self.repo.adicionar(produto)

    def remover_produto(self, id):
        self.repo.remover(id)

    def atualizar_produto(self, produto: Produto):
        self.repo.atualizar(produto)

    def buscar_produto(self, id):
        return self.repo.buscar_por_id(id)

    def listar_produtos(self):
        return self.repo.listar_todos()