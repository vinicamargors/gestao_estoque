from abc import ABC, abstractmethod

class ISugestaoRepository(ABC):
    @abstractmethod
    def salvar(self, sugestao): pass

    @abstractmethod
    def listar_por_produto(self, produto_id): pass

