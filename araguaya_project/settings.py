# araguaya_project/settings.py

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Carrega o .env apenas em ambiente local.
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURAÇÕES DE SEGURANÇA ESSENCIAIS ---

# A SECRET_KEY DEVE vir do ambiente. Se não vier, o app não inicia.
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("A variável de ambiente SECRET_KEY não foi definida.")

# O modo DEBUG é Falso por padrão. Só se torna Verdadeiro se DEBUG=True for definido.
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# --- CONFIGURAÇÃO DE REDE PARA O RAILWAY ---

# Lê os hosts permitidos de uma única variável, separados por vírgula.
# Ex: ALLOWED_HOSTS=meusite.up.railway.app,www.meusite.com
ALLOWED_HOSTS_STR = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR.split(',') if host.strip()]

# Adiciona o host do Railway automaticamente se estiver no ambiente Railway
RAILWAY_STATIC_URL = os.environ.get('RAILWAY_STATIC_URL')
if RAILWAY_STATIC_URL and f'.{RAILWAY_STATIC_URL}' not in ALLOWED_HOSTS:
    # A variável RAILWAY_STATIC_URL contém o nome do host público do app.
    # Ex: web-production-1234.up.railway.app
    ALLOWED_HOSTS.append(f'{RAILWAY_STATIC_URL}')


# CSRF_TRUSTED_ORIGINS é vital para o login no admin funcionar em HTTPS.
# Deve ser uma lista de URLs completos.
CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in ALLOWED_HOSTS]


# --- APLICAÇÕES E MIDDLEWARE (Padrão) ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise é excelente para servir arquivos estáticos de forma eficiente
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'araguaya_project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'araguaya_project.wsgi.application'

# --- CONFIGURAÇÃO DO BANCO DE DADOS (O Ponto Crítico) ---

# Lê a DATABASE_URL do ambiente. Se não existir, a aplicação irá falhar.
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("A variável de ambiente DATABASE_URL não foi definida.")

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True # Forçar SSL é uma boa prática de segurança
    )
}


# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- ARQUIVOS ESTÁTICOS E DE MÍDIA ---

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Pasta onde o collectstatic irá juntar os arquivos
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# Adiciona o storage do Whitenoise para servir arquivos comprimidos e cacheados
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Mídia (Uploads) - Configuração para Google Cloud Storage (se aplicável)
# ... sua configuração do django-storages para GCS continua aqui ...


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'