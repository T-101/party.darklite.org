# --- Builder Stage ---
FROM python:3.13.1-alpine3.21 AS builder

COPY app/requirements.txt /code/app/

RUN pip install uv \
    && uv pip install --prefix=/install -r /code/app/requirements.txt

# --- Final Stage ---
FROM python:3.13.1-alpine3.21

ENV PYTHONUNBUFFERED 1

# Allow postgres container to write logs to volume
RUN ["chmod", "777", "/var/log"]

WORKDIR /code/app/

RUN apk add --no-cache nano tzdata bash logrotate curl

COPY --from=builder /install /usr/local

COPY app/config/partywiki_logrotate.conf /etc/logrotate.d/partywiki
COPY .bashrc /root/
