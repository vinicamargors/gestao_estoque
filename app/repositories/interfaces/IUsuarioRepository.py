from abc import ABC, abstractmethod

class IUsuarioRepository(ABC):
    @abstractmethod
    def adicionar(self, usuario): pass

    @abstractmethod
    def buscar_por_email(self, email): pass

    @abstractmethod
    def listar_todos(self): pass
