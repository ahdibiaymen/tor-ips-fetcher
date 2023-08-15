FROM python:3.8-alpine
ARG build_env=dev

WORKDIR /app

ENV PYTHONPATH=/app/:$PYTHONPATH \
    USERNAME=tor_ip

RUN adduser -D -h /app -u 1000 ${USERNAME}

COPY src ./src
COPY ["wsgi.py","Makefile",".flaskenv","requirements.txt", "./"]
COPY --chown=${USERNAME}:${USERNAME} docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod u+x /docker-entrypoint.sh

RUN apk add --no-cache gcc musl-dev linux-headers \
&& pip install --no-cache-dir -r requirements.txt \
&& pip install uwsgi

USER ${USERNAME}
