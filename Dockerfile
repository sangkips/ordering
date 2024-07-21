ARG PYTHON_VERSION=3.12

# Builder Image
FROM python:${PYTHON_VERSION}-slim-bullseye as builder

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# Final Image
FROM python:${PYTHON_VERSION}-slim-bullseye

ENV APP_HOME=/order \ 
    APP_PORT=8000

RUN mkdir $APP_HOME

WORKDIR $APP_HOME

RUN groupadd -g 1001 order \
    && useradd --no-log-init -r -g order -u 1001 order

RUN apt-get update \
    && apt-get install -yqq --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt ./
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME

RUN mkdir $APP_HOME/logs

RUN chown -R 1001:1001 $APP_HOME

USER 1001

EXPOSE $APP_PORT

CMD ["./run.sh"]
