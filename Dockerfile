FROM python:3.11-slim-bullseye

RUN apt-get update -y\
    && apt-get install -y vim \
    && pip install requests boto3

WORKDIR /var/www
