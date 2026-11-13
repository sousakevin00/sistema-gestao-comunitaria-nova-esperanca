from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Doacao, Entrega, Familia


class FluxoComunitarioTests(TestCase):
    def setUp(self):
        self.familia = Familia.objects.create(responsavel="Família Exemplo", bairro="Centro", integrantes=3)
        self.doacao = Doacao.objects.create(item="Cesta básica", quantidade=5, unidade="cestas", recebida_em=date(2026, 11, 13))

    def test_entrega_reduz_saldo(self):
        Entrega.objects.create(familia=self.familia, doacao=self.doacao, quantidade=2, entregue_em=date(2026, 11, 13))
        self.assertEqual(self.doacao.saldo, 3)

    def test_entrega_acima_do_saldo_e_rejeitada(self):
        with self.assertRaises(ValidationError):
            Entrega.objects.create(familia=self.familia, doacao=self.doacao, quantidade=6, entregue_em=date(2026, 11, 13))
        self.assertEqual(Entrega.objects.count(), 0)

    def test_fluxo_pela_interface(self):
        resposta = self.client.post(reverse("nova_entrega"), {
            "familia": self.familia.pk,
            "doacao": self.doacao.pk,
            "quantidade": 2,
            "entregue_em": "2026-11-13",
            "observacoes": "",
        })
        self.assertRedirects(resposta, reverse("entregas"))
        self.assertContains(self.client.get(reverse("inicio")), "3")
        self.assertContains(self.client.get(reverse("entregas")), "Família Exemplo")
