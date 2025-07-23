from django.contrib import admin
from .models import Peca

@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_insercao', 'dias_em_uso', 'vida_util_restante', 'alerta_substituicao']