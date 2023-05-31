FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential default-libmysqlclient-dev \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000

CMD ["python3", "app/server.py"]
