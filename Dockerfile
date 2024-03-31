# ---- Base Stage ----
FROM python:latest as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

# ---- Copy Stage ----
FROM base as copy-stage

COPY . /app

# --- Testing Stage ---

FROM testing-stage as testing

CMD ["pytest app/src/"]

# ---- Development Stage ----
FROM copy-stage as development

ENV DJANGO_SETTINGS_MODULE=dynatable.settings

CMD ["python", "app/src/manage.py", "runserver", "0.0.0.0:8000"]

# ---- Production Stage ----
FROM copy-stage as production

ENV DJANGO_SETTINGS_MODULE=dynatable.settings

RUN python /app/src/manage.py 

CMD ["gunicorn", "dynatable.wsgi:application", "--bind", "0.0.0.0:8000"]
