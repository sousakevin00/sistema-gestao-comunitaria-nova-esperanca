from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import DoacaoForm, EntregaForm, FamiliaForm
from .models import Doacao, Entrega, Familia


def inicio(request):
    doacoes = list(Doacao.objects.all())
    return render(request, "comunidade/inicio.html", {
        "familias": Familia.objects.count(),
        "doacoes": len(doacoes),
        "entregas": Entrega.objects.count(),
        "doacoes_com_saldo": sum(d.saldo > 0 for d in doacoes),
    })


def familias(request):
    return render(request, "comunidade/lista.html", {
        "titulo": "Famílias", "tipo": "familias", "registros": Familia.objects.all(),
    })


def doacoes(request):
    return render(request, "comunidade/lista.html", {
        "titulo": "Doações", "tipo": "doacoes", "registros": Doacao.objects.all(),
    })


def entregas(request):
    return render(request, "comunidade/lista.html", {
        "titulo": "Entregas", "tipo": "entregas", "registros": Entrega.objects.select_related("familia", "doacao"),
    })


def _formulario(request, form_class, titulo, destino):
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{titulo} registrada com sucesso.")
        return redirect(destino)
    return render(request, "comunidade/formulario.html", {"form": form, "titulo": titulo})


def nova_familia(request):
    return _formulario(request, FamiliaForm, "Família", "familias")


def nova_doacao(request):
    return _formulario(request, DoacaoForm, "Doação", "doacoes")


def nova_entrega(request):
    # A transação mantém a validação e a gravação juntas para o uso local do MVP.
    with transaction.atomic():
        return _formulario(request, EntregaForm, "Entrega", "entregas")
