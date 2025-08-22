# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='home'),
    # Adicione a linha abaixo:
    path('api/semente/<int:semente_id>/', views.semente_api_view, name='semente_api'),
    path('api/solicitar-cotacao/', views.solicitar_cotacao_api_view, name='solicitar_cotacao_api'),
]