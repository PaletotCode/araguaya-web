# core/models.py

from django.db import models

class ConteudoTexto(models.Model):
    chave = models.CharField(max_length=100, unique=True, help_text="Identificador único para o texto (ex: 'hero_titulo'). Não altere.")
    valor = models.TextField(help_text="O texto que aparecerá no site.")

    class Meta:
        verbose_name = "Texto do Site"
        verbose_name_plural = "Textos do Site"

    def __str__(self):
        return self.chave

class HeroSlide(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=300)
    imagem = models.ImageField(upload_to='hero_slides/')
    ordem = models.PositiveIntegerField(default=0, help_text="Use este número para ordenar os slides (0 aparece primeiro).")

    class Meta:
        verbose_name = "Slide da Home"
        verbose_name_plural = "Slides da Home"
        ordering = ['ordem']

    def __str__(self):
        return self.titulo

class Semente(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, help_text="Ex: Brachiaria, Panicum")
    nome_cientifico = models.CharField(max_length=100, verbose_name="Nome Científico")
    imagem = models.ImageField(upload_to='sementes/')
    paragrafo_descricao = models.TextField(verbose_name="Parágrafo de Descrição")
    
    # Especificações Técnicas
    origem = models.CharField(max_length=200, blank=True)
    forma_crescimento = models.CharField(max_length=200, blank=True, verbose_name="Forma de Crescimento")
    altura = models.CharField(max_length=100, blank=True)
    utilizacao = models.CharField(max_length=100, blank=True, verbose_name="Utilização")
    digestibilidade = models.CharField(max_length=100, blank=True)
    palatabilidade = models.CharField(max_length=100, blank=True)
    tolerancia_seca = models.CharField(max_length=100, blank=True, verbose_name="Tolerância à Seca")
    tolerancia_frio = models.CharField(max_length=100, blank=True, verbose_name="Tolerância ao Frio")
    proteina_bruta = models.CharField(max_length=100, blank=True, verbose_name="Proteína Bruta")
    producao_materia_seca = models.CharField(max_length=100, blank=True, verbose_name="Produção de Matéria Seca")
    consorciacao = models.TextField(blank=True, verbose_name="Consorciação")
    pragas = models.TextField(blank=True)
    adubacao_formacao = models.TextField(blank=True, verbose_name="Adubação de Formação")
    aparece_na_comparacao = models.BooleanField(default=False, verbose_name="Aparece na tabela de comparação?", help_text="Marque esta opção para que a semente apareça na tabela 'Compare Nossas Soluções' na home. Recomenda-se marcar no máximo 4.")

    class Meta:
        verbose_name = "Semente"
        verbose_name_plural = "Sementes"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Diferencial(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    icone = models.CharField(max_length=50, help_text="Nome do ícone do Lucide (ex: 'leaf', 'flask-conical', 'award').")
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Diferencial"
        verbose_name_plural = "Diferenciais"
        ordering = ['ordem']

    def __str__(self):
        return self.titulo

class FAQ(models.Model):
    pergunta = models.CharField(max_length=255)
    resposta = models.TextField()
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Pergunta Frequente (FAQ)"
        verbose_name_plural = "Perguntas Frequentes (FAQ)"
        ordering = ['ordem']

    def __str__(self):
        return self.pergunta
    
class ConfiguracoesGerais(models.Model):
    logo_principal = models.ImageField(
        upload_to='config/',
        verbose_name="Logo Principal (Branco)",
        help_text="Logo para usar sobre o banner (geralmente na cor branca).",
        blank=True,
        null=True
    )
    logo_secundario = models.ImageField(upload_to='config/', verbose_name="Logo Secundário (Escuro)", help_text="Logo para usar quando o fundo do menu fica branco (geralmente na cor escura).", blank=True, null=True)
    imagem_fundo_dicas = models.ImageField(upload_to='config/', verbose_name="Imagem de Fundo da Seção 'Qualidade Garantida'")
    mapa_url = models.URLField(max_length=500, verbose_name="URL de Incorporação do Google Maps", help_text="Vá no Google Maps, clique em 'Compartilhar', depois 'Incorporar um mapa' e copie o link que está dentro do atributo 'src'.")
    
    # Informações de Contato
    endereco_rodovia = models.CharField(max_length=255, blank=True)
    endereco_escritorio = models.CharField(max_length=255, blank=True)
    telefone_fixo = models.CharField(max_length=20, blank=True)
    telefone_celular = models.CharField(max_length=20, blank=True, help_text="Incluir o link do WhatsApp se desejar.")
    email_contato = models.EmailField(blank=True)
    # Seção Sobre Nós
    sobre_nos_titulo = models.CharField(max_length=100, blank=True, default="Sobre Nós")
    sobre_nos_p1 = models.TextField(blank=True, verbose_name="Parágrafo 1")
    sobre_nos_p2 = models.TextField(blank=True, verbose_name="Parágrafo 2")
    sobre_nos_p3 = models.TextField(blank=True, verbose_name="Parágrafo 3 (destaque)")
    
    class Meta:
        verbose_name = "Configurações Gerais do Site"
        verbose_name_plural = "Configurações Gerais do Site"

    def __str__(self):
        return "Configurações Gerais do Site"

class ItemNavegacao(models.Model):
    texto = models.CharField(max_length=50)
    link = models.CharField(max_length=100, help_text="Link da âncora (ex: #quemsomos) ou URL completa.")
    ordem = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Item de Navegação"
        verbose_name_plural = "Itens de Navegação"
        ordering = ['ordem']

    def __str__(self):
        return self.texto

class ImagemSobreNos(models.Model):
    configuracao = models.ForeignKey(ConfiguracoesGerais, related_name='imagens_sobre_nos', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='sobre_nos_slides/')
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']
        verbose_name = "Imagem da Seção Sobre Nós"
        verbose_name_plural = "Imagens da Seção Sobre Nós"