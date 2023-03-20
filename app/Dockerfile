FROM python:3.8.2-slim-buster

ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST redis

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y libmagic-dev curl && \
    pip install --upgrade pip && \
    pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

RUN sed -i "s|from werkzeug import secure_filename, FileStorage|from werkzeug.utils import secure_filename\nfrom werkzeug.datastructures import FileStorage|g" /usr/local/lib/python3.8/site-packages/flask_uploads.py

CMD ["celery", "-A", "app.celery", "worker", "--loglevel=INFO"]
c