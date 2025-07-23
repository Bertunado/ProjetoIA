from django.shortcuts import render, redirect
from .models import Peca
from .forms import PecaForm, HistoricoPecaForm
import os
import csv
import joblib
from datetime import datetime, timedelta
from django.conf import settings
from pathlib import Path
import threading
from .treinar_modelo import train_model
import numpy as np


DATA_DIR = Path(__file__).resolve().parent / "ml" / "data"

def peca_registrada(request):
    return render(request, 'manutencao/peca_registrada.html')

def classificar_intensidade(uso_diario):
    if uso_diario < 8.0:
        return 'Leve'
    elif 8.0 <= uso_diario < 15.0:
        return 'Moderado'
    else:
        return 'Intenso'
    
def parse_data(data_str):
    for fmt in ('%d/%m/%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(data_str, fmt).date()
        except (ValueError, TypeError):
            continue
    raise ValueError(f'Formato de data inválido: {data_str}')

def registrar_peca(request):
    resultado = None

    if request.method == 'POST':
        form = HistoricoPecaForm(request.POST)
        if form.is_valid():

            data_troca  = parse_data(request.POST.get('data_troca'))
            data_quebra = parse_data(request.POST.get('data_quebra'))

            if data_quebra < data_troca:
                return render(request, 'manutencao/registrar_peca.html', {
                    'form': form,
                    'resultado': {'erro': 'Data de quebra não pode ser anterior à data de troca.'}
                })

            uso_diario        = float(form.cleaned_data['tempo_uso_diario'])
            descanso_diario   = 24 - uso_diario
            dias_uso          = (data_quebra - data_troca).days
            vida_util_total   = dias_uso

            # — salva no banco (peca_obj já é instância mas ainda não commitado) —
            peca_obj                 = form.save(commit=False)
            peca_obj.data_troca      = data_troca
            peca_obj.data_quebra     = data_quebra
            peca_obj.descanso_diario = descanso_diario
            peca_obj.intensidade_uso = classificar_intensidade(uso_diario)
            peca_obj.save()

            # — salva/atualiza CSV —
            csv_nome = f'dados_{peca_obj.peca}.csv'
            csv_path = Path(settings.BASE_DIR) / csv_nome
            escrever_cabecalho = not csv_path.exists()

            with open(csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f, fieldnames=['uso_diario', 'descanso_diario', 'vida_util_total']
                )
                if escrever_cabecalho:
                    writer.writeheader()
                writer.writerow({
                    'uso_diario'      : uso_diario,
                    'descanso_diario' : descanso_diario,
                    'vida_util_total' : vida_util_total,
                })

            threading.Thread(
                target=train_model, args=(peca_obj.peca,), daemon=True
            ).start()

            resultado = {
                'vida_util_restante': 0,
                'intensidade'       : peca_obj.intensidade_uso,
                'alerta'            : 'Retire a peça imediatamente',
            }

            form = HistoricoPecaForm() 

    else:
        form = HistoricoPecaForm()

    return render(request, 'manutencao/registrar_peca.html', {
        'form'    : form,
        'resultado': resultado
    })

def registrar_uso(request):
    if request.method == 'POST':
        form = HistoricoPecaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('peca_registrada')
    else:
        form = HistoricoPecaForm()
    return render(request, 'manutencao/registrar_peca.html', {'form': form})

def carregar_modelo(peca: str):
    caminho = os.path.join(settings.BASE_DIR, 'ml_models', f'modelo_{peca}.pkl')
    return joblib.load(caminho)

def chat_peca(request):
    pergunta = resposta = None
    data_troca_fmt = data_uso_fmt = periodo_uso = None

    MODEL_DIR = Path(settings.BASE_DIR) / "ml_models"

    try:
        modelo_10 = joblib.load(MODEL_DIR / 'modelo_quantil_10_parafuso.pkl')
        modelo_50 = joblib.load(MODEL_DIR / 'modelo_quantil_50_parafuso.pkl')
        modelo_90 = joblib.load(MODEL_DIR / 'modelo_quantil_90_parafuso.pkl')
    except Exception as e:
        resposta = {'erro': f'Modelos quantílicos não encontrados: {e}'}
        return render(request, 'manutencao/chat.html', {
            'pergunta': None,
            'resposta': resposta,
        })

    if request.method == 'POST':
        tipo           = request.POST.get('peca')
        data_troca_str = request.POST.get('data_troca')
        data_uso_str   = request.POST.get('data_uso')
        uso_diario     = float(request.POST.get('uso_diario', 0))

        try:
            data_troca = parse_data(data_troca_str)
            data_uso = parse_data(data_uso_str)

            data_troca_fmt = data_troca.strftime('%d/%m/%Y')
            data_uso_fmt   = data_uso.strftime('%d/%m/%Y')
            periodo_uso    = f"de {data_troca_fmt} até {data_uso_fmt}"
            dias_uso       = (data_uso - data_troca).days
            descanso_diario = 24 - uso_diario

            pergunta = (
                f"Qual a vida útil de um(a) {tipo} com {dias_uso} dias de uso, "
                f"{uso_diario} h/dia e {descanso_diario} h de descanso?"
            )

            entrada = [[uso_diario, descanso_diario]]

            pred_10 = modelo_10.predict(entrada)[0]
            pred_90 = modelo_90.predict(entrada)[0]
            pred_50 = modelo_50.predict(entrada)[0]


            restante_min     = max(round(pred_10 - dias_uso, 2), 0)
            restante_max     = max(round(pred_90 - dias_uso, 2), 0)
            restante_mediana = max(round(pred_50 - dias_uso, 2), 0)

            percentual_consumido = 0
            if pred_50 > 0:
                percentual_consumido = round((dias_uso / pred_50) * 100, 2)
                percentual_consumido = min(percentual_consumido, 100)

            if percentual_consumido <= 60:
                barra_cor = "bg-success"     #verde
            elif percentual_consumido <= 85:
                barra_cor = "bg-warning"     #amarelo
            else:
                barra_cor = "bg-danger"      #vermelho

            porcentagem_limite = 0.8
            dias_ate_80_porcento = round(pred_50 * porcentagem_limite)
            dias_faltando = dias_ate_80_porcento - dias_uso

            if dias_faltando <= 0:
                data_limite_min = data_uso
            else:
                data_limite_min = data_uso + timedelta(days=dias_faltando)

            data_limite_max = data_uso + timedelta(days=int(restante_max))
            data_limite_mediana = data_uso + timedelta(days=int(restante_mediana))

            data_limite_min = data_limite_min.strftime('%d/%m/%Y')
            data_limite_max = data_limite_max.strftime('%d/%m/%Y')
            data_limite_mediana = data_limite_mediana.strftime('%d/%m/%Y')

            intensidade = classificar_intensidade(uso_diario)
            alerta = 'Substituir imediatamente' if restante_mediana == 0 else 'Ok'

            resposta = {
                'vida_util_restante': restante_mediana,
                'intervalo_estimado': f"{restante_min} a {restante_max} dias",
                'data_limite_min': data_limite_min,
                'data_limite_max': data_limite_max,
                'data_limite_media': data_limite_mediana,
                'intensidade': intensidade,
                'alerta': alerta,
                'dias_uso': dias_uso,
                'percentual_consumido': percentual_consumido,
                'barra_cor': barra_cor,
            }

        except Exception as e:
            resposta = {'erro': f'Erro ao processar dados: {e}'}

    return render(
        request,
        'manutencao/chat.html',
        {
            'pergunta': pergunta,
            'resposta': resposta,
            'data_troca_formatada': data_troca_fmt,
            'data_uso_formatada': data_uso_fmt,
            'periodo_uso': periodo_uso,
        },
    )

def escolher_peca(request):
    pecas_opcoes = ['parafuso', 'correia', 'ventosa']
    if request.method == 'POST':
        escolha = request.POST.get('peca')
        return redirect('lista_pecas_filtrada', tipo_peca=escolha)
    return render(request, 'manutencao/escolher_peca.html', {'pecas_opcoes': pecas_opcoes})

def lista_pecas_filtrada(request, tipo_peca):
    pecas = Peca.objects.filter(nome__iexact=tipo_peca)
    return render(request, 'manutencao/lista_pecas.html', {'pecas': pecas, 'tipo_peca': tipo_peca})

def lista_pecas(request):
    pecas = Peca.objects.all()
    return render(request, 'manutencao/lista_pecas.html', {'pecas': pecas})

def adiciona_peca(request):
    if request.method == 'POST':
        form = PecaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pecas')
    else:
        form = PecaForm()
    return render(request, 'manutencao/adiciona_peca.html', {'form': form})