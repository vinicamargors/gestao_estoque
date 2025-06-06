from app.repositories.interfaces.IEstoqueRepository import IEstoqueRepository
from app.models.Produto import Produto

class EstoqueService:
    def __init__(self, repo: IEstoqueRepository):
        self.repo = repo

    def carregar_estoque(self):
        return self.repo.carregar_estoque()

    def adicionar_produto(self, produto: Produto):
        self.repo.salvar_produto(produto)

    def remover_produto(self, id_produto):
        self.repo.deletar_produto(id_produto)
