release: python manage.py migrate && python manage.py createsuperuser --noinput
web: gunicorn araguaya_project.wsgi