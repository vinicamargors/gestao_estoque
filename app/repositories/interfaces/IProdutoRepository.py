from abc import ABC, abstractmethod

class IProdutoRepository(ABC):
    @abstractmethod
    def adicionar(self, produto): pass

    @abstractmethod
    def remover(self, id_produto): pass

    @abstractmethod
    def atualizar(self, produto): pass

    @abstractmethod
    def buscar_por_id(self, id_produto): pass

    @abstractmethod
    def listar_todos(self): pass