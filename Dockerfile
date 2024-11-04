FROM python:3.10

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* /app/

RUN pip install -U pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root

COPY . /app
ENV PYTHONPATH=/app

RUN chmod +x run.sh