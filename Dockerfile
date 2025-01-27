FROM python:3.13.1-alpine3.21

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code/app/

RUN apk add --no-cache nano tzdata bash build-base logrotate
ENV TZ=Europe/Helsinki

# Allow postgres container to write logs to volume
RUN ["chmod", "777", "/var/log"]

COPY app/requirements.txt /code/app/
RUN pip install -r requirements.txt

RUN pip install --upgrade pip

COPY partywiki_logrotate.conf /etc/logrotate.d/partywiki
COPY .bashrc /root/
COPY crontab.txt /crontab.txt
RUN /usr/bin/crontab /crontab.txt

ADD . /code/

# CMD ["/bin/sh", "-c", "gunicorn config.wsgi --timeout 600 -w $UWSGI_WORKERS -b 0.0.0.0:$CONTAINER_PORT"]
