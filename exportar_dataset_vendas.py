import sqlite3
import csv
from datetime import datetime

# Caminho do banco
conexao = sqlite3.connect('estoque.db')  # troque se o nome for diferente
cursor = conexao.cursor()

# Seleciona dados da tabela de histórico de vendas
cursor.execute("""
    SELECT nome, categoria, fornecedor, quantidade_vendida, preco_base, preco_venda, data_validade, data_venda
    FROM vendas
""")

dados = cursor.fetchall()

# Nome do arquivo CSV
nome_csv = 'vendas_dataset.csv'

# Cabeçalho do CSV
cabecalho = [
    'nome',
    'categoria',
    'fornecedor',
    'quantidade_vendida',
    'dias_para_vencer',
    'preco_base',
    'preco_venda'
]

# Abre e escreve o arquivo CSV
with open(nome_csv, 'w', newline='', encoding='utf-8') as arquivo:
    writer = csv.writer(arquivo)
    writer.writerow(cabecalho)

    for linha in dados:
        nome, categoria, fornecedor, qtd, preco_base, preco_venda, validade, venda = linha

        # Calcula dias entre validade e venda
        try:
            data_validade = datetime.strptime(validade, '%Y-%m-%d')
            data_venda = datetime.strptime(venda, '%Y-%m-%d')
            dias_para_vencer = (data_validade - data_venda).days
        except:
            dias_para_vencer = 0  # caso datas estejam mal formatadas

        writer.writerow([
            nome,
            categoria,
            fornecedor,
            qtd,
            dias_para_vencer,
            preco_base,
            preco_venda
        ])

print(f"✅ Dados exportados com sucesso para: {nome_csv}")
