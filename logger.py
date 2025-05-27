import os
from datetime import datetime

def registrar_log(acao, usuario="Sistema"):
    # Cria pasta "log" se não existir
    os.makedirs("log", exist_ok=True)

    # Define caminho do arquivo de log
    caminho_log = os.path.join("log", "registro_geral.txt")

    # Formata o horário e a mensagem
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = f"[{agora}] USUÁRIO: {usuario} | AÇÃO: {acao}\n"

    # Escreve no arquivo
    with open(caminho_log, "a", encoding="utf-8") as f:
        f.write(linha)
