# The builder image, used to build the virtual environment
FROM python:3.10-buster as builder
# Install Poetry
RUN pip install poetry==1.7.1
# Set the Poetry environment variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache
# Set the working directory
WORKDIR /app
# Copy the codebase to the working directory
COPY api/ api/
COPY cookiecutterplus/ cookiecutterplus/
COPY persistence/ persistence/
# Copy the pyproject.toml, poetry.lock, README.md, and LICENSE to the working directory
COPY pyproject.toml poetry.lock README.md LICENSE ./
# Install the dependencies
RUN poetry install --no-dev && poetry build && rm -rf $POETRY_CACHE_DIR


# The runtime image, used to just run the code provided its virtual environment
FROM python:3.10-slim-buster as runtime
WORKDIR /app
# Install git and gh
RUN apt-get update \
    && apt-get install -y --no-install-recommends git gnupg software-properties-common curl \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y --no-install-recommends gh \
    && git config --global credential.helper '!gh auth git-credential' \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# Set the runtime environment variables
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    OUTPUT_BASE=/app/output/ \
    PYTHONUNBUFFERED=1
# Copy the virtual environment from the builder image
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
# Copy the codebase to the working directory
COPY api/ api/
COPY cookiecutterplus/ cookiecutterplus/
COPY persistence/ persistence/
# Expose the API port
EXPOSE 5000

RUN python -m venv ${VIRTUAL_ENV} 

ENTRYPOINT [ "cookiecutterplus", "-a", "true" ]
