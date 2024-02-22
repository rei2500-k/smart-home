FROM python:3.11-slim-bullseye

RUN apt-get update -y\
    && apt-get install -y vim \
    && pip install requests

WORKDIR /var/www
