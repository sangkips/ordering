FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN apt update && apt install -y g++ libpq-dev gcc musl-dev

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tc4a.wsgi.application", "-w", "2"]
