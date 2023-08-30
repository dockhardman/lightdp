FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y curl docker.io build-essential && \
    apt-get clean && \
    python -m pip install --upgrade pip

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
