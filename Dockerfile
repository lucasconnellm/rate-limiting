FROM python:3.9.2-slim-buster

ARG POETRY_VERSION=1.1.13
ENV POETRY_VERSION=${POETRY_VERSION}

COPY . /app/
WORKDIR /app/

RUN pip install --upgrade pip && pip install poetry==${POETRY_VERSION} && poetry install

EXPOSE 8000

CMD [ "poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0" ]
