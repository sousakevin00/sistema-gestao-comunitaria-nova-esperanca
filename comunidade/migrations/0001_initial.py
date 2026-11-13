from django.core.validators import MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Doacao",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("item", models.CharField(max_length=120)),
                ("quantidade", models.PositiveIntegerField(validators=[MinValueValidator(1)])),
                ("unidade", models.CharField(default="unidade(s)", max_length=30)),
                ("recebida_em", models.DateField(verbose_name="recebida em")),
                ("observacoes", models.TextField(blank=True, verbose_name="observações")),
            ],
            options={"verbose_name": "doação", "verbose_name_plural": "doações", "ordering": ["-recebida_em", "item"]},
        ),
        migrations.CreateModel(
            name="Familia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("responsavel", models.CharField(max_length=120, verbose_name="responsável")),
                ("bairro", models.CharField(max_length=100)),
                ("integrantes", models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])),
                ("observacoes", models.TextField(blank=True, verbose_name="observações")),
                ("cadastrada_em", models.DateTimeField(auto_now_add=True)),
            ],
            options={"verbose_name": "família", "verbose_name_plural": "famílias", "ordering": ["responsavel"]},
        ),
        migrations.CreateModel(
            name="Entrega",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantidade", models.PositiveIntegerField(validators=[MinValueValidator(1)])),
                ("entregue_em", models.DateField(verbose_name="entregue em")),
                ("observacoes", models.TextField(blank=True, verbose_name="observações")),
                ("doacao", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="entregas", to="comunidade.doacao")),
                ("familia", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="entregas", to="comunidade.familia")),
            ],
            options={"verbose_name": "entrega", "verbose_name_plural": "entregas", "ordering": ["-entregue_em", "-id"]},
        ),
    ]
