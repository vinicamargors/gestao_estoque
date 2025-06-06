from abc import ABC, abstractmethod

class IVendaRepository(ABC):
    @abstractmethod
    def registrar(self, venda): pass

    @abstractmethod
    def listar_todas(self): pass

    @abstractmethod
    def buscar_por_id(self, id_venda): pass

    @abstractmethod
    def listar_por_produto(self, produto_id): pass

    @abstractmethod
    def listar_por_periodo(self, data_inicio, data_fim): pass
