from abc import ABC, abstractmethod

class IEstoqueRepository(ABC):
    @abstractmethod
    def carregar_estoque(self): pass

    @abstractmethod
    def salvar_produto(self, produto): pass

    @abstractmethod
    def deletar_produto(self, id_produto): pass