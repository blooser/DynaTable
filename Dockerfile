# ---- Base Stage ----
FROM python:latest as base

LABEL title="DynaTable"
LABEL description="Dynamic models for django"
LABEL version="0.0.1"
LABEL author="Mateusz Solnica (blooser@protonmail.com)"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

# ---- Copy Stage ----
FROM base as copy-stage

COPY . /app

# ---- Development Stage ----
FROM copy-stage as development

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=dynatable.settings

CMD ["python", "app/src/manage.py", "runserver", "0.0.0.0:8000"]

# ---- Production Stage ----
FROM copy-stage as production

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=dynatable.settings

RUN python /app/src/manage.py 

CMD ["gunicorn", "dynatable.wsgi:application", "--bind", "0.0.0.0:8000"]
