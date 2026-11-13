from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("familias/", views.familias, name="familias"),
    path("familias/nova/", views.nova_familia, name="nova_familia"),
    path("doacoes/", views.doacoes, name="doacoes"),
    path("doacoes/nova/", views.nova_doacao, name="nova_doacao"),
    path("entregas/", views.entregas, name="entregas"),
    path("entregas/nova/", views.nova_entrega, name="nova_entrega"),
]
