import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from django.conf import settings

MODEL_DIR = os.path.join(settings.BASE_DIR, 'ml_models')
os.makedirs(MODEL_DIR, exist_ok=True)

def train_model(peca: str) -> None:
    print(f"🔁 Re-treinando modelo da peça: {peca}")
    caminho_csv = f'dados_{peca}.csv'
    if not os.path.isfile(caminho_csv):
        raise FileNotFoundError(f"Arquivo {caminho_csv} não encontrado.")

    dados = pd.read_csv(caminho_csv)
    dados.columns = dados.columns.str.strip()

    colunas_esperadas = ['uso_diario', 'descanso_diario', 'vida_util_total']
    if not set(colunas_esperadas).issubset(dados.columns):
        raise ValueError(f"Colunas incorretas no arquivo {caminho_csv}. Encontradas: {dados.columns.tolist()}")

    dados = dados[colunas_esperadas].apply(pd.to_numeric, errors='coerce').dropna()

    if len(dados) < 2:
        raise ValueError(f"Poucos dados válidos para treinar o modelo de {peca}.")

    X = dados[['uso_diario', 'descanso_diario']]
    y = dados['vida_util_total']

    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X, y)

    caminho_modelo = os.path.join(MODEL_DIR, f'modelo_{peca}.pkl')
    joblib.dump(modelo, caminho_modelo)
    print(f" Modelo de {peca} treinado e salvo.")

if __name__ == "__main__":
    pecas = ['parafuso', 'correia', 'ventosa']
    for peca in pecas:
        try:
            print(f"\n🔧 Treinando modelo para: {peca}")
            train_model(peca)
        except Exception as e:
            print(f" Erro ao treinar modelo de {peca}: {e}")