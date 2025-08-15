FROM ghcr.io/astral-sh/uv:python3.11-alpine

WORKDIR /src

ENV UV_COMPILE_BYTECODE=1

RUN uv venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ../pyproject.toml /src/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=../pyproject.toml,target=/src/pyproject.toml \
    uv sync --no-dev

COPY src /src
EXPOSE 8000
