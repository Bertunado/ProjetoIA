from django import forms
from .models import Peca, HistoricoPeca

class PecaForm(forms.ModelForm):
    class Meta:
        model = Peca
        fields = '__all__'
        widgets = {
            'data_insercao': forms.DateInput(attrs={'type': 'date'}),
        }

class HistoricoPecaForm(forms.ModelForm):
    class Meta:
        model = HistoricoPeca
        fields = ['peca', 'data_troca', 'data_quebra', 'tempo_uso_diario', 'tipo_manutencao']
        widgets = {
            'peca': forms.Select(attrs={'class': 'form-control'}),
            'data_troca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dd/mm/aaaa', 'id': 'data_troca'}),
            'data_quebra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dd/mm/aaaa', 'id': 'data_quebra'}),
            'tempo_uso_diario': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'tipo_manutencao': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_tempo_uso_diario(self):
        valor = self.cleaned_data['tempo_uso_diario']
        if not (0 <= valor <= 24):
            raise forms.ValidationError('Informe um valor entre 0 e 24 horas.')
        return valor