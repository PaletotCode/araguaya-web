# core/admin.py
from django.contrib import admin
from .models import ConteudoTexto, HeroSlide, Semente, Diferencial, FAQ, ConfiguracoesGerais, ItemNavegacao,  ImagemSobreNos

@admin.register(ConteudoTexto)
class ConteudoTextoAdmin(admin.ModelAdmin):
    list_display = ('chave', 'valor')
    search_fields = ('chave', 'valor')
    list_per_page = 20

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtitulo', 'ordem')
    list_editable = ('ordem',)

@admin.register(Semente)
class SementeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'proteina_bruta', 'tolerancia_seca')
    list_filter = ('tipo',)
    search_fields = ('nome', 'nome_cientifico')
    fieldsets = (
        ('Informações Principais', {
            'fields': ('nome', 'tipo', 'nome_cientifico', 'imagem', 'paragrafo_descricao')
        }),
        ('Especificações Técnicas', {
            'classes': ('collapse',),
            'fields': (
                'origem', 'forma_crescimento', 'altura', 'utilizacao', 'digestibilidade',
                'palatabilidade', 'tolerancia_seca', 'tolerancia_frio', 'proteina_bruta',
                'producao_materia_seca', 'consorciacao', 'pragas', 'adubacao_formacao'
            ),
        }),
    )

@admin.register(Diferencial)
class DiferencialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'icone', 'ordem')
    list_editable = ('ordem',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'ordem')
    list_editable = ('ordem',)

class ImagemSobreNosInline(admin.TabularInline):
    model = ImagemSobreNos
    extra = 1 # Quantos campos de upload de imagem vazios aparecem por padrão

@admin.register(ConfiguracoesGerais)
class ConfiguracoesGeraisAdmin(admin.ModelAdmin):
    inlines = [ImagemSobreNosInline]

    def has_add_permission(self, request):
        return not ConfiguracoesGerais.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(ItemNavegacao)
class ItemNavegacaoAdmin(admin.ModelAdmin):
    list_display = ('texto', 'link', 'ordem')
    list_editable = ('ordem',)