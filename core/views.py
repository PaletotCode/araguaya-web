# core/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import ConteudoTexto, HeroSlide, Semente, Diferencial, FAQ, ConfiguracoesGerais, ItemNavegacao

import json
from django.views.decorators.csrf import csrf_exempt

def index_view(request: HttpRequest) -> HttpResponse:
    """
    Busca todos os objetos de conteúdo do banco de dados e renderiza a página inicial.
    """
    # Tenta buscar as configurações gerais. Se não existir, retorna None.
    try:
        configuracoes = ConfiguracoesGerais.objects.get()
    except ConfiguracoesGerais.DoesNotExist:
        configuracoes = None

    slides_qs = HeroSlide.objects.all()
    for i, slide in enumerate(slides_qs):
        slide.animation_delay = i * 4

    diferenciais = Diferencial.objects.all()
    sementes = Semente.objects.all()
    sementes_comparacao = Semente.objects.filter(aparece_na_comparacao=True)
    faqs = FAQ.objects.all()
    itens_navegacao = ItemNavegacao.objects.all()
    
    textos_qs = ConteudoTexto.objects.all()
    textos = {item.chave: item.valor for item in textos_qs}
    
    context = {
        'config': configuracoes, # Nome curto para facilitar no template
        'slides': slides_qs,
        'diferenciais': diferenciais,
        'sementes': sementes,
        'sementes_comparacao': sementes_comparacao,
        'faqs': faqs,
        'itens_navegacao': itens_navegacao,
        'textos': textos,
    }
    
    return render(request, 'index.html', context)

def semente_api_view(request: HttpRequest, semente_id: int) -> JsonResponse:
    """
    Busca uma única semente pelo seu ID e retorna seus dados em formato JSON.
    """
    semente = get_object_or_404(Semente, pk=semente_id)
    
    # Monta um dicionário com os dados que o JavaScript precisa
    data = {
        'id': semente.id,
        'nome': semente.nome,
        'nome_cientifico': semente.nome_cientifico,
        'paragrafo_descricao': semente.paragrafo_descricao,
        'imagem_url': semente.imagem.url,
        'origem': semente.origem,
        'forma_crescimento': semente.forma_crescimento,
        'altura': semente.altura,
        'utilizacao': semente.utilizacao,
        'digestibilidade': semente.digestibilidade,
        'palatabilidade': semente.palatabilidade,
        'tolerancia_seca': semente.tolerancia_seca,
        'tolerancia_frio': semente.tolerancia_frio,
        'proteina_bruta': semente.proteina_bruta,
        'producao_materia_seca': semente.producao_materia_seca,
        'consorciacao': semente.consorciacao,
        'pragas': semente.pragas,
        'adubacao_formacao': semente.adubacao_formacao,
    }
    return JsonResponse(data)

@csrf_exempt # Usado para simplificar o POST via API. Em produção, use um método de autenticação mais robusto.
def solicitar_cotacao_api_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome = data.get('nome')
            contato = data.get('contato')
            produto = data.get('produto')
            mensagem = data.get('mensagem')

            # --- AÇÃO COMERCIAL ACONTECE AQUI ---
            # Por enquanto, vamos apenas imprimir no console para confirmar o recebimento.
            print("--- NOVA SOLICITAÇÃO DE COTAÇÃO ---")
            print(f"Nome: {nome}")
            print(f"Contato: {contato}")
            print(f"Produto: {produto}")
            print(f"Mensagem: {mensagem}")
            print("------------------------------------")
            # Em um projeto real, aqui você enviaria um e-mail para a equipe de vendas.

            return JsonResponse({'status': 'sucesso', 'mensagem': 'Sua solicitação foi enviada com sucesso!'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'erro', 'mensagem': 'Dados inválidos.'}, status=400)
    
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido.'}, status=405)
