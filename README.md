# LangChain-OCR

**LangChain-OCR** is an advanced OCR solution that converts PDFs and image files into Markdown using cutting-edge vision LLMs. The project comprises two main components: the OCR library (usable via CLI) and a FastAPI backend that offers a streamlined interface for file uploads and processing.

<div align="center">
  <img src="./images/ocr-logo.png" alt="OCR Logo" style="width:30%;">
</div>

## Table of Contents

1. [Overview](#1-overview)
2. [Features](#2-features)
3. [Installation](#3-installation)
   1. [Prerequisites](#31-prerequisites)
   2. [Cloning & Environment Setup](#32-cloning--environment-setup)
4. [Usage](#4-usage)
   1. [CLI](#41-cli)
   2. [FastAPI Server](#42-fastapi-server)
   3. [Docker Compose Deployment](#43-docker-compose-deployment)
5. [Contributing](#5-contributing)
6. [License](#6-license)
7. [Contact](#7-contact)

## 1. Overview

LangChain-OCR leverages vision LLMs to deliver high-quality OCR conversion from PDFs and images (JPEG, PNG) into Markdown. With support for both a direct CLI and an asynchronous FastAPI interface, it serves as a versatile tool for developers and end-users.

## 2. Features

- **File Conversion:** Convert PDFs and images (JPEG, PNG) to Markdown.
- **Extensible Design:** Easily customize converters, language models, and dependency injections with [Inject](https://pypi.org/project/Inject/).
- **Modern API:** Asynchronous processing built on FastAPI.
- **Observability:** Integrated tracing via [Langfuse](https://langfuse.com/).
- **Multilingual Support:** Configurable language settings.
- **LLM Integration:** Supports [Ollama](https://ollama.com/) with potential for other providers.
- **Containerization:** Ready-to-use Docker and Docker Compose configurations.
- **CLI Access:** Quick OCR processing through the command line.

## 3. Installation

### 3.1. Prerequisites

- **Python:** 3.11 or higher (refer to [api/.python-version](api/.python-version))
- **Dependency Manager:** [Poetry](https://python-poetry.org/)
- **Docker & Docker Compose:** For containerized deployment

### 3.2. Cloning & Environment Setup

Clone the repository and configure your environment:

```bash
git clone https://github.com/a-klos/langchain-ocr.git
cd langchain-ocr
cp .env.template .env
```

Edit the `.env` file as necessary to adjust language settings, model configuration, and endpoints.

## 4. Usage

LangChain-OCR can be employed in different ways:

### 4.1. CLI

For quick OCR tasks via the command line, see the [CLI documentation](langchain_ocr_lib/README.md).

### 4.2. FastAPI Server

Launch the FastAPI backend to access OCR functionality through a RESTful API. Detailed instructions are provided in the [FastAPI README](api/README.md).

### 4.3. Docker Compose Deployment

Deploy the entire stack with Docker Compose:

1. **Install Docker Compose:**  
   Follow the [installation guide](https://docs.docker.com/compose/install/).

2. **Build & Run Containers:**  
   In the repository root, execute:
   ```bash
   docker compose up --build
   ```

3. **Pull a Vision-Capable Model:**  
   Ensure your model configuration matches by pulling the model (e.g., `x/llama3.2-vision:11b-instruct-fp16`):
   ```bash
   ollama pull <<model_name>>
   ```

4. **Access the Services:**  
   - **FastAPI Interface:** [http://localhost:8001/docs](http://localhost:8001/docs)  
   - **Langfuse Dashboard:** [http://localhost:3000](http://localhost:3000)  
     (Default credentials: **Username:** user, **Password:** password123 – update as needed.)

5. **Stop Containers:**  
   When done, clean up with:
   ```bash
   docker compose down
   ```

## 5. Contributing

Contributions, bug reports, and feature suggestions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get involved.

## 6. License

Licensed under the MIT License. Refer to the [LICENSE](LICENSE) file for more information.

## 7. Contact

For questions, issues, or suggestions, please open an issue on GitHub or contact the maintainer at `aklos.ocr@gmail.com`
.
