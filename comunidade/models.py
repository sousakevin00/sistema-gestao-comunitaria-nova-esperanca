from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum


class Familia(models.Model):
    responsavel = models.CharField("responsável", max_length=120)
    bairro = models.CharField(max_length=100)
    integrantes = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    observacoes = models.TextField("observações", blank=True)
    cadastrada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["responsavel"]
        verbose_name = "família"
        verbose_name_plural = "famílias"

    def __str__(self):
        return self.responsavel


class Doacao(models.Model):
    item = models.CharField(max_length=120)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unidade = models.CharField(max_length=30, default="unidade(s)")
    recebida_em = models.DateField("recebida em")
    observacoes = models.TextField("observações", blank=True)

    class Meta:
        ordering = ["-recebida_em", "item"]
        verbose_name = "doação"
        verbose_name_plural = "doações"

    def __str__(self):
        return f"{self.item} ({self.quantidade} {self.unidade})"

    @property
    def saldo(self):
        entregues = self.entregas.aggregate(total=Sum("quantidade"))["total"] or 0
        return self.quantidade - entregues

    def clean(self):
        if self.pk and self.quantidade is not None:
            entregues = self.entregas.aggregate(total=Sum("quantidade"))["total"] or 0
            if self.quantidade < entregues:
                raise ValidationError({"quantidade": "Quantidade menor que o total já entregue."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Entrega(models.Model):
    familia = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name="entregas")
    doacao = models.ForeignKey(Doacao, on_delete=models.PROTECT, related_name="entregas")
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    entregue_em = models.DateField("entregue em")
    observacoes = models.TextField("observações", blank=True)

    class Meta:
        ordering = ["-entregue_em", "-id"]
        verbose_name = "entrega"
        verbose_name_plural = "entregas"

    def __str__(self):
        return f"{self.familia} — {self.doacao.item}"

    def clean(self):
        if self.quantidade is not None and self.quantidade < 1:
            raise ValidationError({"quantidade": "Informe uma quantidade maior que zero."})
        if self.doacao_id and self.quantidade:
            total = self.doacao.entregas.exclude(pk=self.pk).aggregate(total=Sum("quantidade"))["total"] or 0
            if total + self.quantidade > self.doacao.quantidade:
                raise ValidationError({"quantidade": "Quantidade maior que o saldo disponível da doação."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
