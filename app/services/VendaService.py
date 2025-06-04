from app.models.Venda import Venda
from app.repositories.interfaces.IVendaRepository import IVendaRepository

class VendaService:
    def __init__(self, repo: IVendaRepository):
        self.repo = repo

    def registrar_venda(self, id, produto_id, quantidade, preco_unitario):
        venda = Venda(id, produto_id, quantidade, 0)
        venda.calcular_total(preco_unitario)
        self.repo.registrar(venda)

    def listar_vendas(self):
        return self.repo.listar_todas()

    def buscar_venda(self, id):
        return self.repo.buscar_por_id(id)

    def listar_vendas_por_produto(self, produto_id):
        return self.repo.listar_por_produto(produto_id)

    def listar_vendas_por_periodo(self, data_inicio, data_fim):
        return self.repo.listar_por_periodo(data_inicio, data_fim)
