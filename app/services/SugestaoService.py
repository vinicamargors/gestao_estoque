from app.models.Sugestao import Sugestao
from datetime import datetime, timedelta
import joblib
import numpy as np

class SugestaoService:
    def __init__(self, produto_repo, venda_repo, sugestao_repo, modelo_path="modelo_margem.pkl"):
        self.produto_repo = produto_repo
        self.venda_repo = venda_repo
        self.sugestao_repo = sugestao_repo
        self.modelo = joblib.load(modelo_path)

    def analisar_e_gerar_sugestoes(self):
        produtos = self.produto_repo.listar_todos()
        hoje = datetime.today()
        inicio_mes = hoje.replace(day=1)

        for produto in produtos:
            if "perecivel" not in produto.categoria.lower():
                continue

            vendas = self.venda_repo.listar_por_produto(produto.id)
            vendas_mes = [v for v in vendas if datetime.strptime(v.data_venda, "%Y-%m-%d %H:%M:%S") >= inicio_mes]

            if not vendas_mes:
                continue  # Não sugere para produtos sem movimentação

            dias_ultima_venda = (hoje - max([datetime.strptime(v.data_venda, "%Y-%m-%d %H:%M:%S") for v in vendas])).days
            entrada = np.array([[len(vendas_mes), produto.quantidade, dias_ultima_venda]])
            margem = round(float(self.modelo.predict(entrada)[0]), 2)
            preco_sugerido = round(produto.preco_unitario * (1 + margem), 2)

            sugestao = Sugestao(
                produto_id=produto.id,
                quantidade_sugerida=produto.quantidade,
                preco_sugerido=preco_sugerido,
                margem_usada=margem
            )
            self.sugestao_repo.salvar(sugestao)
