FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN apt-get update \
    && apt-get install -y libpq-dev \
    && pip3 install --upgrade pip \
    && pip3 install gunicorn \
    && pip3 install -r requirements.txt --no-cache-dir

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "python_meetup.wsgi:application", "--bind", "0:8000"]
