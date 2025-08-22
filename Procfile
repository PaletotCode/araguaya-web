release: echo "Iniciando a fase release..." && echo "DATABASE_URL encontrada: $DATABASE_URL" && python manage.py migrate
web: gunicorn araguaya_project.wsgi