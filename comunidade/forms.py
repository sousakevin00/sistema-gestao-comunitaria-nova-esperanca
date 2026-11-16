from django import forms
from django.db.models import F, Sum
from django.db.models.functions import Coalesce

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        campo_doacao = self.fields["doacao"]
        campo_doacao.queryset = Doacao.objects.annotate(
            saldo_disponivel=F("quantidade") - Coalesce(Sum("entregas__quantidade"), 0)
        )
        campo_doacao.label_from_instance = lambda doacao: (
            f"{doacao.item} — saldo disponível: {doacao.saldo_disponivel} {doacao.unidade}"
        )

    class Meta:
        model = Entrega
        fields = ["familia", "doacao", "quantidade", "entregue_em", "observacoes"]
        widgets = {"entregue_em": forms.DateInput(attrs={"type": "date"})}
        labels = {"familia": "Família", "doacao": "Doação"}
