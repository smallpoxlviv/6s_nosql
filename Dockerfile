# syntax=docker/dockerfile:1

FROM python:3.10-alpine

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip3 install poetry
RUN poetry install

COPY . .

EXPOSE 8080

CMD [ "python3", "nosql"]