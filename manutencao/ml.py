import joblib
import os
from django.conf import settings

ml_path = os.path.join(settings.BASE_DIR, 'ml_models')

# Carrega os modelos separados
try:
    modelo_parafuso = joblib.load(os.path.join(ml_path, 'modelo_parafuso.pkl'))
except FileNotFoundError:
    modelo_parafuso = None
    print(" modelo_parafuso.pkl não encontrado.")

try:
    modelo_correia = joblib.load(os.path.join(ml_path, 'modelo_correia.pkl'))
except FileNotFoundError:
    modelo_correia = None
    print(" modelo_correia.pkl não encontrado.")

try:
    modelo_ventosa = joblib.load(os.path.join(ml_path, 'modelo_ventosa.pkl'))
except FileNotFoundError:
    modelo_ventosa = None
    print(" modelo_ventosa.pkl não encontrado.")

def calcular_vida_util_restante(peca):
    
    if peca.tipo == 'parafuso' and modelo_parafuso is not None:
        dados = [[peca.uso_diario, peca.descanso_diario]]
        previsao = modelo_parafuso.predict(dados)
    elif peca.tipo == 'correia' and modelo_correia is not None:
        dados = [[peca.uso_diario, peca.descanso_diario]]
        previsao = modelo_correia.predict(dados)
    elif peca.tipo == 'ventosa' and modelo_ventosa is not None:
        dados = [[peca.uso_diario, peca.descanso_diario]]
        previsao = modelo_ventosa.predict(dados)
    else:
        return 0 

    return max(int(previsao[0]), 0)