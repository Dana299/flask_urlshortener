FROM python:3.10.12-slim

ENV PYTHONDONTWRITEBYCODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 

RUN pip install poetry==1.6.1

WORKDIR /
COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev

COPY . .

ENTRYPOINT ["poetry", "run", "python", "main.py"]

