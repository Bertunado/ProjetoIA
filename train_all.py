import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import joblib
import os

model_dir = 'ml_models'
os.makedirs(model_dir, exist_ok=True)

pecas = ['parafuso', 'correia', 'ventosa']

for peca in pecas:
    print(f"\nTreinando modelos para: {peca}")

    caminho_csv = f'dados_{peca}.csv'
    if not os.path.isfile(caminho_csv):
        print(f"Arquivo {caminho_csv} não encontrado, pulando...")
        continue

    dados = pd.read_csv(caminho_csv)
    dados.columns = dados.columns.str.strip()

    colunas_esperadas = ['uso_diario', 'descanso_diario', 'vida_util_total']
    if not set(colunas_esperadas).issubset(dados.columns):
        print(f"Colunas incorretas no arquivo {caminho_csv}. Encontradas: {dados.columns.tolist()}")
        continue

    dados = dados[colunas_esperadas].apply(pd.to_numeric, errors='coerce').dropna()

    if len(dados) < 10:
        print(f"Poucos dados para treinar modelo de {peca}, pulando...")
        continue

    X = dados[['uso_diario', 'descanso_diario']]
    y = dados['vida_util_total']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    params = {
        'objective': 'quantile',
        'metric': 'quantile',
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.1,
        'min_data_in_leaf': 20,
    }

    quantis = [0.1, 0.5, 0.9]
    modelos = {}

    for q in quantis:
        print(f" Treinando quantil {q}")
        params['alpha'] = q
        train_data = lgb.Dataset(X_train, label=y_train)
        model = lgb.train(params, train_data, num_boost_round=100)
        modelos[q] = model
        # Salva modelo
        joblib.dump(model, os.path.join(model_dir, f'modelo_quantil_{int(q*100)}_{peca}.pkl'))

    for q, model in modelos.items():
        preds = model.predict(X_test)
        print(f"Modelo quantil {q} para {peca} treinado.")

print("Treinamento finalizado.")