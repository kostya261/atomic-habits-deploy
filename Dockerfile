FROM python:3.13-alpine

WORKDIR /app

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/app/.venv/bin:$PATH"

RUN pip install --no-cache-dir poetry==1.8

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --only main

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]