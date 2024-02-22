FROM python:3.12

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-root

COPY . /app

CMD ["poetry", "run", "python", "bot.py"]
