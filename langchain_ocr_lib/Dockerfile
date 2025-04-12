FROM --platform=linux/amd64 python:3.11.11-bookworm AS builder

ENV POETRY_VIRTUALENVS_PATH=/app/.venv
ENV POETRY_VERSION=2.1.2

WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential --no-install-recommends make && \
    python3 -m venv "${POETRY_VIRTUALENVS_PATH}"
RUN $POETRY_VIRTUALENVS_PATH/bin/pip install "poetry==${POETRY_VERSION}"
ENV PATH="${POETRY_VIRTUALENVS_PATH}/bin:$PATH"

COPY langchain_ocr_lib .

RUN poetry config virtualenvs.create false &&\
    poetry install --no-interaction --no-ansi

FROM --platform=linux/amd64 python:3.11.11-bookworm

ENV POETRY_VIRTUALENVS_PATH=/app/.venv

WORKDIR /app

COPY --from=builder ${POETRY_VIRTUALENVS_PATH} ${POETRY_VIRTUALENVS_PATH}
ENV PATH="${POETRY_VIRTUALENVS_PATH}/bin:$PATH"

COPY langchain_ocr_lib .

ENTRYPOINT ["langchain-ocr"]