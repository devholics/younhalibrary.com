FROM python:3.9-bullseye

WORKDIR /usr/src/app

RUN apt-get update && apt-get install --assume-yes --no-install-recommends postgresql-client-13

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python -
RUN ln -s /etc/poetry/bin/poetry /usr/local/bin/poetry
RUN poetry config virtualenvs.create false

RUN python -m pip install libsass

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
RUN poetry install --no-root

COPY ./docker-entrypoint.sh ./docker-entrypoint.sh

COPY . .

ENTRYPOINT ["./docker-entrypoint.sh"]
