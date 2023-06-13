# Younha Library

[![Build Status](https://github.com/devholics/younhalibrary.com/actions/workflows/test-younha.yml/badge.svg?branch=main)](https://github.com/devholics/younhalibrary.com/actions/workflows/test-younha.yml)

Younha Library source code

## Local development guide

You will run a development server at http://localhost:8000/. Three main sites are:

- Main - http://localhost:8000/
- Django admin - http://localhost:8000/admin/
- REST API - http://api.localhost:8000/

For the REST API, you need to add `127.0.0.1 api.localhost` to your `/etc/hosts`.

### With Docker Compose

The easiest way to run locally is to use [Docker Compose](https://docs.docker.com/compose/).

1. Build the images:
    ```shell
    docker compose build
    ```
2. Run the containers:
    ```shell
    docker compose up
    ```
3. View http://localhost:8000/
4. (Optional) To access Django admin, create superuser:
    ```shell
    docker compose exec web python manage.py createsuperuser
    ```

### Without Docker

Without Docker, you'll need [Poetry](https://python-poetry.org/) and [Sass](https://sass-lang.com/).

1. Install Python 3.9 (or higher).
2. [Install Poetry](https://python-poetry.org/docs/#installation)
3. Install dependencies:
    ```shell
    poetry install
    ```
4. Migrate database:
    ```shell
    poetry run python manage.py migrate
    ```
5. Compile SCSS:
    ```shell
    sass ./younhalibrary/scss/main.scss ./younhalibrary/static/css/main.scss
    ```
6. (Optional) Load `medialib` test database:
    ```shell
    poetry run python manage.py loaddata medialib_live_data
    ```
7. (Optional) To access Django admin, create superuser:
    ```shell
    poetry run python manage.py createsuperuser
    ```