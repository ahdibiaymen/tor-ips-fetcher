FROM python:3.8-alpine
ARG build_env=dev

WORKDIR app/src

ENV PYTHONPATH=/app/src:$PYTHONPATH

COPY requirements.txt .

RUN apk add --no-cache gcc musl-dev linux-headers \
&& pip install --no-cache-dir -r requirements.txt \
&& pip install uwsgi

COPY src .
RUN mv wsgi.py ../



