# araguaya_project/urls.py

from django.contrib import admin
from django.urls import path, include  # Adicione 'include' aqui
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Apenas para ambiente de desenvolvimento local
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# No final do arquivo, fora de urlpatterns
admin.site.site_header = "Painel de Administração Araguaya"
admin.site.site_title = "Administração Araguaya"
admin.site.index_title = "Bem-vindo ao painel de controle"