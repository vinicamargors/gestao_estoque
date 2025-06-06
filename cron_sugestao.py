import schedule
import time
from app.repositories.ProdutoRepository import ProdutoRepository
from app.repositories.VendaRepository import VendaRepository
from app.repositories.SugestaoRepository import SugestaoRepository
from app.services.SugestaoService import SugestaoService

def executar_sugestao():
    print("[INFO] Iniciando sugestão automatizada...")
    produto_repo = ProdutoRepository()
    venda_repo = VendaRepository()
    sugestao_repo = SugestaoRepository()
    sugestao_service = SugestaoService(produto_repo, venda_repo, sugestao_repo)
    sugestao_service.analisar_e_gerar_sugestoes()
    print("[INFO] Sugestões geradas com sucesso.")

# Roda todos os dias às 3h da manhã
schedule.every().day.at("06:00").do(executar_sugestao)

print("[INFO] Agendador de sugestão iniciado. Aguardando horário...")
while True:
    schedule.run_pending()
    time.sleep(60)