from django.contrib import admin

from .models import Doacao, Entrega, Familia

admin.site.register(Familia)
admin.site.register(Doacao)
admin.site.register(Entrega)
