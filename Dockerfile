FROM python:3.9-alpine as build

WORKDIR /usr/src/app

RUN apk add --no-cache build-base libpq-dev python3-dev
RUN pip install poetry

RUN python -m venv /opt/venv
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install libsass

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install

FROM python:3.9-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache libpq python3

COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
COPY . .

ENV PORT=8080
ENV DJANGO_SETTINGS_MODULE=younhalibrary.settings.docker

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD gunicorn younhalibrary.wsgi -b 0.0.0.0:$PORT

