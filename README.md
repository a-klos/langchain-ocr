# LangChain-OCR

<p align="center">
   <a href="https://github.com/a-klos/langchain-ocr/blob/aec379b25dc101accc04a0b0568ecf95fca26a48/LICENSE">
   <img src="https://img.shields.io/badge/License-MIT-E11311.svg" alt="MIT License">
   </a>
   <a href="https://pypi.org/project/langchain-ocr-lib/">
  <img src="https://img.shields.io/pypi/dm/langchain-ocr-lib?logo=python&logoColor=white&label=pypi%20langchain-ocr-lib&color=blue" alt="langchain-ocr-lib Python package on PyPi">
   </a>
   <a href="https://discord.gg/98dTaPgR" target="_blank">
   <img src="https://img.shields.io/discord/1361307926677028864?logo=discord&labelColor=%20%235462eb&logoColor=%20%23f5f5f5&color=%20%235462eb"
      alt="chat on Discord">
   </a>
   <a href="https://www.linkedin.com/in/andreas-klos/" target="_blank">
   <img src="https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff" alt="follow on LinkedIn">
   </a>   
   <br>
   <a href="https://github.com/a-klos/langchain-ocr/graphs/commit-activity" target="_blank">
   <img alt="Commits last month" src="https://img.shields.io/github/commit-activity/m/a-klos/langchain-ocr?labelColor=%20%2332b583&color=%20%2312b76a"></a>
   <a href="https://github.com/a-klos/langchain-ocr-lib/" target="_blank">
   <img alt="Issues closed" src="https://img.shields.io/github/issues-search?query=repo%3Aa-klos%2Flangchain-ocr%20is%3Aclosed&label=issues%20closed&labelColor=%20%237d89b0&color=%20%235d6b98"></a>
   <a href="https://github.com/a-klos/langchain-ocr/discussions/" target="_blank">
   <img alt="Discussion posts" src="https://img.shields.io/github/discussions/a-klos/langchain-ocr?labelColor=%20%239b8afb&color=%20%237a5af8"></a>
</p>

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
   4. [Gradio UI](#44-gradio-ui)
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
- **LLM Integration:** Supports [Ollama](https://ollama.com/), [vLLM](https://docs.vllm.ai/en/latest/) and [OpenAI](https://openai.com/api/) with potential for other providers.
- **Containerization:** Ready-to-use Docker and Docker Compose configurations.
- **CLI Access:** Quick OCR processing through the command line.

## 3. Installation

### 3.1 Prerequisites

- **Python:** 3.11 or higher (refer to [api/.python-version](api/.python-version))
- **Dependency Manager:** [Poetry](https://python-poetry.org/)
- **Docker & Docker Compose:** For containerized deployment

### 3.2 Cloning & Environment Setup

Clone the repository and configure your environment:

```bash
git clone https://github.com/a-klos/langchain-ocr.git
cd langchain-ocr
cp .env.template .env
```

Edit the `.env` file as necessary to adjust language settings, model configuration, and endpoints.

## 4. Usage

LangChain-OCR can be employed in different ways:

### 4.1 CLI

For quick OCR tasks via the command line, see the [CLI documentation](langchain_ocr_lib/README.md).

### 4.2 FastAPI Server

Launch the FastAPI backend to access OCR functionality through a RESTful API. Detailed instructions are provided in the [FastAPI README](api/README.md).

### 4.3 Docker Compose Deployment

Deploy the entire stack with Docker Compose:

1. **Install Docker Compose:**  
   Follow the [installation guide](https://docs.docker.com/compose/install/).

2. **Build & Run Containers:**  
   In the repository root, execute:
   ```bash
   docker compose up --build
   ```

3. **Pull a Vision-Capable Model:**  
   Ensure your model configuration matches by pulling the model (e.g., `gemma3:4b-it-q4_K_M`):
   ```bash
   ollama pull <<model_name>>
   ```

4. **Access the Services:**  
   - **FastAPI Interface:** [http://0.0.0.0:8081/docs](http://0.0.0.0:8081/docs)  
   - **Langfuse Dashboard:** [http://localhost:3000](http://localhost:3000)  
     (Default credentials: **Username:** user, **Password:** password123 – update as needed.)

5. **Stop Containers:**  
   When done, clean up with:
   ```bash
   docker compose down
   ```

### 4.4 Gradio UI

Access OCR functionality through an intuitive browser interface:

1. **Online Demo:**
   Try the hosted version at [Hugging Face Spaces](https://huggingface.co/spaces/skynet1010/LangChain-OCR-Playground) without any installation.

2. **Local Deployment:**
   Configure the environment variables in `gradio_ui/.env` and`run the Gradio app:
   ```bash
   cd gradio_ui
   poetry install --no-root
   set -a
   source .env
   set +a
   cd src/gradio_ui
   python app.py
   ```

## 5. Contributing

Contributions, bug reports, and feature suggestions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get involved.

## 6. License

Licensed under the MIT License. Refer to the [LICENSE](LICENSE) file for more information.

## 7. Contact

For questions, issues, or suggestions, please open an issue on GitHub or contact the maintainer at `aklos.ocr@gmail.com`.
