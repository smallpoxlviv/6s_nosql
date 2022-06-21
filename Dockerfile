# syntax=docker/dockerfile:1

FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip3 install poetry
RUN poetry install

COPY . .

EXPOSE 8080

CMD [ "python3", "nosql"]