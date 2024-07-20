FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=tc4a.settings

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git-core \
    build-essential \
    binutils \
    libproj-dev \
    gdal-bin \
    supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY requirements .
RUN mkdir -p /usr/src/app/media
WORKDIR /usr/src/app

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

EXPOSE 8000

RUN mkdir -p /var/logs/ordering

COPY ./deployment/scripts /home/docker/scripts
COPY ./deployment/configs/supervisor-backend.conf /etc/supervisor/conf.d/supervisor-backend.conf

RUN sed -i 's/\r$//' /home/docker/scripts/boot.sh  && \
    chmod +x /home/docker/scripts/boot.sh

COPY . .

ENTRYPOINT /home/docker/scripts/boot.sh


