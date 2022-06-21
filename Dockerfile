# syntax=docker/dockerfile:1

FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_NO_INTERACTION=1

WORKDIR /app

RUN pip3 install poetry

# Install python dependencies in /.venv
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

EXPOSE 8081

ENTRYPOINT ["python3", "nosql"]