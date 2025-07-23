import joblib
import os

model_dir = 'ml_models'
pecas = ['parafuso', 'correia', 'ventosa']

for peca in pecas:
    caminho_modelo = os.path.join(model_dir, f'modelo_{peca}.pkl')
    if not os.path.exists(caminho_modelo):
        print(f" Modelo de {peca} não encontrado.")
        continue

    try:
        modelo = joblib.load(caminho_modelo)
        n_features = modelo.n_features_in_
        print(f" Modelo '{peca}' espera {n_features} feature(s).")
    except Exception as e:
        print(f" Erro ao carregar modelo '{peca}': {e}")
