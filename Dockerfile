FROM python:3.9.2-alpine3.13

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code/app/

RUN apk add nano tzdata bash build-base
RUN cp /usr/share/zoneinfo/Europe/Helsinki /etc/localtime
RUN echo "Europe/Helsinki" > /etc/timezone

COPY app/requirements.txt /code/app/
RUN pip install -r requirements.txt
ADD . /code/

RUN pip install --upgrade pip

ADD crontab.txt /crontab.txt
RUN /usr/bin/crontab /crontab.txt

# CMD ["/bin/sh", "-c", "gunicorn config.wsgi --timeout 600 -w $UWSGI_WORKERS -b 0.0.0.0:$CONTAINER_PORT"]
