# API

FastAPI backend that exposes an HTTP interface for the `langchain_ocr_lib` — converting PDFs and image files into Markdown using vision-enabled LLMs like `gemma3` via LangChain and Ollama (other LLM providers will follow).

## Features

- RESTful OCR API using FastAPI
- Input: PDF, PNG, JPG, JPEG
- Output: Markdown-formatted text
- Powered by `langchain_ocr_lib`
- Containerized with Docker

---

## Installation

### Prerequisites

- **Python:** 3.11 or higher (refer to [api/.python-version](api/.python-version))
- **Dependency Manager:** [Poetry](https://python-poetry.org/)
- **Ollama:** For LLM model serving
- **Docker:** For containerized deployment (optional)

## Usage

### Local Dev

```bash
cd api
poetry install --with dev
PYTHONPATH=src uvicorn langchain_ocr.main:app --host 0.0.0.0 --port 8080
```

Then open:  
[http://localhost:8080/docs](http://localhost:8080/docs)

> *NOTE*: If you tryout the endpoints, you might see the following output in the terminal -- the terminal in which you have executed the uvicorn command:

>Error while fetching prompt 'OcrChain-label:production': [Errno -2] Name or service not known

That means, that the Langfuse service is not running/reachable. Prompt management is done via Langfuse, but if Langfuse is not available, the default (fallback) prompt and LLM will be used.

### Environment Variables

Configured via `.env` or directly in shell:

The configurable environment variables are shown in [`../.env.template`](../.env.template).

The `.env.template` file is a template for the environment variables. You can copy it to `.env` and adjust the values as needed. Afterwards, you can run the server with the command:
```bash
PYTHONPATH=src uvicorn langchain_ocr.main:app --host 0.0.0.0 --port 8080 --env-file .env
```

---

## Build and Run with Docker

Build the Docker image from the root of the repository:

```bash
docker build -t api -f api/Dockerfile .
```

After building the image, run the container:

```bash
docker run --net=host -it --rm api
```

API will be accessible at:  
[http://localhost:8080/docs](http://localhost:8080/docs)

>*NOTE*: The environment variables can be passed to the container via the `--env-file` option. For example:
```bash
docker run --net=host -it --rm --env-file .env api
```

Make sure to run or pull the vision model locally:

```bash
ollama pull gemma3
```

---

## Integration: `langchain_ocr`

This FastAPI layer is a thin wrapper around the core [`langchain_ocr_lib`](https://github.com/a-klos/langchain-ocr/tree/28205adddc252a29901a98079c3703d27ea80a46/langchain_ocr_lib) Python package.

Any updates to OCR logic, file handling, or model configuration happen in the library, not here.
