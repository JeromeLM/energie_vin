FROM python:3.10-slim

RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir /app

WORKDIR /app/src
