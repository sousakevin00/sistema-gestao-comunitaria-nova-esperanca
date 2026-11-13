from django import forms

from .models import Doacao, Entrega, Familia


class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        fields = ["responsavel", "bairro", "integrantes", "observacoes"]


class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ["item", "quantidade", "unidade", "recebida_em", "observacoes"]
        widgets = {"recebida_em": forms.DateInput(attrs={"type": "date"})}


class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ["familia", "doacao", "quantidade", "entregue_em", "observacoes"]
        widgets = {"entregue_em": forms.DateInput(attrs={"type": "date"})}
