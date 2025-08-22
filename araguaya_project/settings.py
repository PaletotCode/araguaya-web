import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env em ambiente de desenvolvimento
# O Railway irá ignorar isso e usar suas próprias variáveis de ambiente
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CHAVE SECRETA ---
# Lê a SECRET_KEY das variáveis de ambiente.
# É crucial para a segurança em produção.
SECRET_KEY = os.environ.get('SECRET_KEY')

# --- MODO DEBUG ---
# Desativa o DEBUG automaticamente quando em produção.
# O valor 'False' é mais seguro. '1' ou 'True' só devem ser usados localmente.
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')

# --- HOSTS PERMITIDOS ---
# Lê os hosts permitidos das variáveis de ambiente.
# Você já configurou "web-production-53d55.up.railway.app" no seu painel.
ALLOWED_HOSTS_STR = os.environ.get('ALLOWED_HOSTS')
ALLOWED_HOSTS = ALLOWED_HOSTS_STR.split(',') if ALLOWED_HOSTS_STR else []

# --- CSRF (Cross-Site Request Forgery) ---
# Necessário para que o Django confie em requisições seguras (HTTPS) do Railway.
CSRF_TRUSTED_ORIGINS_STR = os.environ.get('CSRF_TRUSTED_ORIGINS')
if CSRF_TRUSTED_ORIGINS_STR:
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in CSRF_TRUSTED_ORIGINS_STR.split(',')]
else:
    # Se a variável de ambiente CSRF_TRUSTED_ORIGINS não for definida,
    # podemos usar os ALLOWED_HOSTS como um fallback seguro.
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Suas aplicações
    'core.apps.CoreConfig',
    
    # Aplicações de terceiros
    'storages', # Para gerenciar arquivos de mídia no GCS
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
        'DIRS': [BASE_DIR / 'templates'], # Certifique-se que sua pasta de templates está aqui
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


# --- BANCO DE DADOS ---
# Configuração mágica para o Railway.
# O dj-database-url lê a variável DATABASE_URL e configura tudo para você.
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600, # Mantém as conexões persistentes para melhor performance
        ssl_require=True # Força SSL, essencial para segurança em produção
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- ARQUIVOS ESTÁTICOS (CSS, JS, etc.) ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles_build" # Pasta para coletar arquivos estáticos para produção

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CONFIGURAÇÃO DE MÍDIA (Uploads de Imagens para o Google Cloud Storage) ---
# Adicione estas variáveis de ambiente no seu painel do Railway.
# Ex: GOOGLE_CLOUD_STORAGE_BUCKET_NAME = 'seu-bucket-name'
#     GOOGLE_CLOUD_STORAGE_PROJECT_ID = 'seu-project-id'
#     GOOGLE_APPLICATION_CREDENTIALS_JSON = 'conteúdo do seu JSON de credenciais'

if 'GOOGLE_CLOUD_STORAGE_BUCKET_NAME' in os.environ:
    # Esta configuração só será ativada se as variáveis do GCS existirem.
    # Isso permite que você use o armazenamento local em desenvolvimento.
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = os.environ.get('GOOGLE_CLOUD_STORAGE_BUCKET_NAME')
    GS_PROJECT_ID = os.environ.get('GOOGLE_CLOUD_STORAGE_PROJECT_ID')
    
    # A maneira mais segura de passar as credenciais para o Railway
    # é via uma única variável de ambiente contendo o JSON completo.
    # No painel do Railway, cole o conteúdo do seu arquivo .json nessa variável.
    gcs_credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if gcs_credentials_json:
        import json
        from google.oauth2 import service_account
        
        credentials_info = json.loads(gcs_credentials_json)
        GS_CREDENTIALS = service_account.Credentials.from_service_account_info(credentials_info)

    MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
    MEDIA_ROOT = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'