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
        self.assertEqual(self.client.get(reverse("inicio")).context["doacoes_com_saldo"], 1)
        self.assertContains(self.client.get(reverse("entregas")), "Família Exemplo")

    def test_edicao_nao_pode_reduzir_doacao_abaixo_do_entregue(self):
        Entrega.objects.create(familia=self.familia, doacao=self.doacao, quantidade=3, entregue_em=date(2026, 11, 13))
        self.doacao.quantidade = 2
        with self.assertRaises(ValidationError):
            self.doacao.save()
        self.doacao.refresh_from_db()
        self.assertEqual(self.doacao.quantidade, 5)

    def test_formulario_rejeita_entrega_sem_saldo(self):
        resposta = self.client.post(reverse("nova_entrega"), {
            "familia": self.familia.pk,
            "doacao": self.doacao.pk,
            "quantidade": 6,
            "entregue_em": "2026-11-13",
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Quantidade maior que o saldo disponível")
        self.assertEqual(Entrega.objects.count(), 0)

    def test_painel_conta_doacoes_com_saldo(self):
        Entrega.objects.create(familia=self.familia, doacao=self.doacao, quantidade=5, entregue_em=date(2026, 11, 13))
        self.assertEqual(self.client.get(reverse("inicio")).context["doacoes_com_saldo"], 0)
        Doacao.objects.create(item="Arroz", quantidade=10, unidade="kg", recebida_em=date(2026, 11, 13))
        self.assertEqual(self.client.get(reverse("inicio")).context["doacoes_com_saldo"], 1)

    def test_formulario_rejeita_doacao_zero(self):
        resposta = self.client.post(reverse("nova_doacao"), {
            "item": "Feijão", "quantidade": 0, "unidade": "kg", "recebida_em": "2026-11-13",
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.context["form"].errors)
        self.assertEqual(Doacao.objects.count(), 1)

