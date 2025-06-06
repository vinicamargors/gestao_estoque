import pandas as pd
import joblib
import os
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

# Caminho do modelo
modelo_path = "modelo_margem.pkl"

# Carregar novos dados
novos_dados = pd.read_csv("data/historico_vendas.csv")
X_novo = novos_dados[["qtd_vendas_mes", "estoque_atual", "dias_desde_ultima_venda"]]
y_novo = novos_dados["margem_real"]

# Verifica se o modelo já existe
if os.path.exists(modelo_path):
    print("[INFO] Modelo existente encontrado. Carregando...")
    pipeline = joblib.load(modelo_path)
else:
    print("[INFO] Nenhum modelo existente. Criando novo modelo...")
    # SGDRegressor suporta treinamento incremental (online learning)
    regressor = SGDRegressor(max_iter=1000, tol=1e-3)
    pipeline = make_pipeline(StandardScaler(), regressor)

# Treinamento incremental (partial_fit)
# Como partial_fit exige y numérico contínuo, podemos treinar diretamente
pipeline.fit(X_novo, y_novo)

# Avaliação simples
score = pipeline.score(X_novo, y_novo)
print(f"[INFO] Score atualizado do modelo com novos dados: {round(score, 4)}")

# Salva o modelo atualizado
joblib.dump(pipeline, modelo_path)
print("[INFO] Modelo atualizado salvo com sucesso.")
