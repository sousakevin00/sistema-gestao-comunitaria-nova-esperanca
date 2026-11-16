from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.http import HttpResponse
from django.db import connection


def healthz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        return HttpResponse("unavailable", status=503, content_type="text/plain")
    return HttpResponse("ok", content_type="text/plain")

urlpatterns = [
    path("healthz/", healthz, name="healthz"),
    path("login/", auth_views.LoginView.as_view(template_name="comunidade/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("", include("comunidade.urls")),
]
