FROM python:3.11

COPY . /code
WORKDIR /code
EXPOSE 8000

RUN apt-get update
RUN apt-get install -y nano
RUN pip install -r requirements.txt

CMD python manage.py migrate \
        && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')" \
        && python manage.py collectstatic --no-input \
        && gunicorn music_site.wsgi:application --bind 0.0.0.0:8000 --log-level info