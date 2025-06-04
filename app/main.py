from app.repositories.ProdutoRepository import ProdutoRepository
from app.repositories.VendaRepository import VendaRepository
from app.repositories.SugestaoRepository import SugestaoRepository
from app.services.SugestaoService import SugestaoService

if __name__ == "__main__":
    produto_repo = ProdutoRepository()
    venda_repo = VendaRepository()
    sugestao_repo = SugestaoRepository()

    sugestao_service = SugestaoService(produto_repo, venda_repo, sugestao_repo)
    sugestao_service.analisar_e_gerar_sugestoes()

    print("\nSugestões de precificação geradas com sucesso!")
