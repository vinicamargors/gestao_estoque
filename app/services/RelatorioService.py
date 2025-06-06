from app.models.Relatorio import Relatorio

class RelatorioService:
    def gerar_relatorio_estoque(self, produtos):
        dados = [p.to_dict() for p in produtos]
        return Relatorio("Estoque", dados)

    def gerar_relatorio_vendas(self, vendas):
        dados = [v.to_dict() for v in vendas]
        return Relatorio("Vendas", dados)

    def salvar_relatorio(self, relatorio, caminho):
        relatorio.salvar_em_arquivo(caminho)
