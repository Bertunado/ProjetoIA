from django.db import models
from django.utils import timezone
from .ml import calcular_vida_util_restante

class HistoricoPeca(models.Model):
    PECA_CHOICES = [
        ('parafuso', 'Parafuso'),
        ('correia', 'Correia'),
        ('ventosa', 'Ventosa'),
    ]

    INTENSIDADE_CHOICES = [
        ('leve', 'Leve'),
        ('moderado', 'Moderado'),
        ('intenso', 'Intenso'),
    ]

    MANUT_CHOICES = [
        ('preventiva', 'Preventiva'),
        ('corretiva' , 'Corretiva'),
        ('melhoria'  , 'Melhoria/Upgrade'),
    ]

    peca = models.CharField(max_length=20, choices=PECA_CHOICES)
    data_troca = models.DateField()
    data_quebra = models.DateField()
    tempo_uso_diario = models.FloatField()
    descanso_diario = models.FloatField()
    tipo_manutencao = models.CharField(max_length=15, choices=MANUT_CHOICES, default='corretiva')
    intensidade_uso = models.CharField(max_length=10, choices=INTENSIDADE_CHOICES, null=True, blank=True)

    vida_util_restante = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.peca} - {self.data_troca}"

    @property
    def vida_util_restante_calculada(self):
        return calcular_vida_util_restante(self)

class Peca(models.Model):
    nome = models.CharField(max_length=100)
    data_insercao = models.DateField()
    uso_diario = models.FloatField()
    descanso_diario = models.FloatField()

    @property
    def dias_em_uso(self):
        return (timezone.now().date() - self.data_insercao).days

    @property
    def vida_util_restante(self):
        return calcular_vida_util_restante(self)

    @property
    def alerta_substituicao(self):
        return "Substituir" if self.vida_util_restante <= 0 else "Ok"
