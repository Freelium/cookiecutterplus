FROM python:3.10-buster as builder

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY api/ api/
COPY cookiecutterplus/ cookiecutterplus/

COPY pyproject.toml poetry.lock README.md LICENSE ./

RUN poetry install --no-dev && poetry build && rm -rf $POETRY_CACHE_DIR


# The runtime image, used to just run the code provided its virtual environment
FROM python:3.10-slim-buster as runtime
WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY api/ api/
COPY cookiecutterplus/ cookiecutterplus/

EXPOSE 5000

RUN python -m venv ${VIRTUAL_ENV} 

ENTRYPOINT [ "cookiecutterplus", "-a", "true" ]
