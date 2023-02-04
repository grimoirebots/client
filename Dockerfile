FROM python:3.11.1-slim

# Python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# Poetry settings
ENV POETRY_VERSION=1.3.2
ENV POETRY_HOME=/etc/poetry
ENV POETRY_VIRTUALENVS_CREATE=false

# Docker settings
ENV VERSION=20.10.23

# Install OS packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH=$POETRY_HOME/bin:$PATH

# Install Docker
RUN curl -fsSL https://get.docker.com | sh -

WORKDIR /code

# Install dependencies
COPY poetry.lock pyproject.toml /code/
RUN poetry install --no-root

# Copy Grimoirebots files
COPY . /code/
RUN poetry install --only-root

CMD ["python", "-m", "grimoirebots_client"]
