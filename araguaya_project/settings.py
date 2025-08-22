import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (para desenvolvimento local)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta e modo Debug lidos das variáveis de ambiente
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Hosts permitidos são lidos de uma variável de ambiente (ex: "meusite.up.railway.app,localhost")
# Lógica robusta para ALLOWED_HOSTS que se adapta ao Railway e ao desenvolvimento local
ALLOWED_HOSTS = []

# Adiciona o domínio público do Railway automaticamente, se existir
if RAILWAY_STATIC_URL := os.getenv('RAILWAY_STATIC_URL'):
    ALLOWED_HOSTS.append(RAILWAY_STATIC_URL)

# Permite adicionar outros domínios (como seu domínio personalizado no futuro)
if MANUAL_HOSTS := os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS.extend(MANUAL_HOSTS.split(','))

# Permite acesso local se o DEBUG estiver ativado
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

# Para produção, o Railway injeta o CSRF_TRUSTED_ORIGINS, mas podemos adicionar manualmente se necessário
# Lógica robusta para CSRF_TRUSTED_ORIGINS
csrf_origins_env = os.getenv('CSRF_TRUSTED_ORIGINS')
CSRF_TRUSTED_ORIGINS = csrf_origins_env.split(',') if csrf_origins_env else []

railway_url = os.getenv('RAILWAY_STATIC_URL')
if railway_url:
    CSRF_TRUSTED_ORIGINS.append('https://' + railway_url)

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
    'whitenoise.middleware.WhiteNoiseMiddleware', # Essencial para servir arquivos estáticos em produção
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

# Configuração de Banco de Dados CORRIGIDA para Railway (PostgreSQL) ou local (SQLite)
database_url = os.getenv('DATABASE_URL', '')

if database_url:
    # Para produção (Railway com PostgreSQL)
    DATABASES = {
        'default': dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
            options={
                'charset': 'utf8',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'options': {
                    'charset': 'utf8mb4',
                }
            }
        )
    }
    
    # FORÇAR CODIFICAÇÃO UTF-8 PARA POSTGRESQL
    DATABASES['default']['OPTIONS'] = {
        'charset': 'utf8',
    }
    
    # Adicionar configurações específicas para PostgreSQL
    if DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
        DATABASES['default']['OPTIONS'].update({
            'client_encoding': 'UTF8',
            'default_transaction_isolation': 'read committed',
            'timezone': 'UTC',
        })
else:
    # Para desenvolvimento local (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Forçar codificação UTF-8 em todo o Django
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

# Arquivos de Mídia (Uploads de usuário via Admin)
# Serão servidos pelo Google Cloud Storage
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'

# Arquivos Estáticos (CSS, JS do projeto, imagens fixas)
# Serão servidos pelo WhiteNoise
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'