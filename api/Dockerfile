FROM --platform=linux/amd64 python:3.11.7-bookworm AS builder

ENV POETRY_VIRTUALENVS_PATH=/app/.venv
ENV POETRY_VERSION=2.1.2

WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential --no-install-recommends make && \
    python3 -m venv "${POETRY_VIRTUALENVS_PATH}" \
    && $POETRY_VIRTUALENVS_PATH/bin/pip install "poetry==${POETRY_VERSION}"
ENV PATH="${POETRY_VIRTUALENVS_PATH}/bin:$PATH"
ENV VIRTUAL_ENV="${POETRY_VIRTUALENVS_PATH}"

COPY langchain_ocr_lib langchain_ocr_lib

COPY api api

WORKDIR /app/api

RUN poetry config virtualenvs.create false &&\
    poetry install --no-interaction --no-ansi 

FROM --platform=linux/amd64 python:3.11.7-bookworm

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends poppler-utils

ENV POETRY_VIRTUALENVS_PATH=/app/.venv
ENV VIRTUAL_ENV="${POETRY_VIRTUALENVS_PATH}"


WORKDIR /app


COPY --from=builder /app/.venv /app/.venv
ENV PATH="${POETRY_VIRTUALENVS_PATH}/bin:$PATH"

COPY api api

WORKDIR /app/api

CMD ["/app/.venv/bin/python", "-m", "uvicorn", "src.langchain_ocr.main:app", "--host", "0.0.0.0", "--port", "8080"]
