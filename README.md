# Araguaya Sementes - Web Application

Este repositório contém o código-fonte da aplicação web da Araguaya Sementes, desenvolvida em Python com o framework Django. O projeto foi estruturado para ser robusto, seguro e facilmente gerenciável através de um painel de administração intuitivo.

## Missão do Projeto

Desenvolver e implantar, em 48 horas, uma aplicação web de nível comercial com um back-office para gerenciamento de conteúdo. A solução final é otimizada para ser facilmente compreendida, mantida e expandida por desenvolvedores ou uma IA assistente.

## Tech Stack

-   **Framework:** Django
-   **Servidor de Aplicação (Produção):** Gunicorn
-   **Banco de Dados:** PostgreSQL
-   **Armazenamento de Mídia:** Google Cloud Storage (GCS)
-   **Dependências Principais:**
    -   `psycopg2-binary`: Adaptador para PostgreSQL.
    -   `python-dotenv`: Gerenciamento de variáveis de ambiente local.
    -   `dj-database-url`: Parse de URL de banco de dados.
    -   `django-storages` & `google-cloud-storage`: Integração com GCS.

## Setup e Instalação Local

Para executar este projeto em um ambiente de desenvolvimento local, siga os passos abaixo.

**1. Clone o Repositório**

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd araguaia-web
```

**2. Crie e Ative o Ambiente Virtual**

Isso garante que as dependências do projeto fiquem isoladas.

* **Windows:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
* **macOS / Linux:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

**3. Instale as Dependências**

O arquivo `requirements.txt` contém todos os pacotes necessários.

```bash
pip install -r requirements.txt
```

**4. Configure as Variáveis de Ambiente**

Crie um arquivo chamado `.env` na raiz do projeto. Ele guardará suas chaves e configurações locais. Comece com a configuração do banco de dados (recomenda-se usar PostgreSQL localmente via Docker ou instalação direta).

```ini
# Exemplo de conteúdo para .env
DEBUG=True
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DATABASE_NAME
```

**5. Execute as Migrações do Banco de Dados**

Este comando cria as tabelas no banco de dados com base nos modelos definidos no código.

```bash
python manage.py migrate
```

**6. Crie um Superusuário**

Você usará este usuário para acessar o painel de administração (`/admin`).

```bash
python manage.py createsuperuser
```

## Rodando o Servidor de Desenvolvimento

Após a configuração, inicie o servidor local do Django.

```bash
python manage.py runserver
```

A aplicação estará disponível em `http://127.0.0.1:8000/`.
O painel de administração estará em `http://127.0.0.1:8000/admin/`.

## Deploy

Este projeto está pré-configurado para deploy na plataforma [Railway](https://railway.app/). A implantação é gerenciada através do arquivo `Procfile` e das variáveis de ambiente configuradas diretamente no serviço do Railway.# araguaya-web
