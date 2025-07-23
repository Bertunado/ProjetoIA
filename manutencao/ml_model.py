import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Dados fictícios para o treinamento inicial
dados = {
    'dias_em_uso': [10, 50, 100, 150, 200, 250],
    'uso_diario': [2, 3, 4, 5, 6, 7],
    'descanso_diario': [22, 21, 20, 19, 18, 17],
    'vida_util_total': [300, 300, 300, 300, 300, 300],
    'vida_util_restante': [290, 240, 190, 140, 90, 40]
}

df = pd.DataFrame(dados)

X = df[['dias_em_uso', 'uso_diario', 'descanso_diario', 'vida_util_total']]
y = df['vida_util_restante']

modelo = LinearRegression()
modelo.fit(X, y)

joblib.dump(modelo, 'modelo_vida_util.pkl')