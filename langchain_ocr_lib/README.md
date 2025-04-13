# langchain-ocr-lib

**langchain-ocr-lib** is the OCR processing engine behind LangChain-OCR. It provides a modular, vision-LLM-powered Chain to convert image and PDF documents into clean Markdown. Designed for direct CLI usage or integration into larger applications.

<div align="center">
  <img src="./images/logo.png" alt="Logo" style="width:30%;">
</div>

## Table of Contents

1. [Overview](#1-overview)
2. [Features](#2-features)
3. [Installation](#3-installation)
   1. [Prerequisites](#31-prerequisites)
   2. [Environment Setup](#32-environment-setup)
4. [Usage](#4-usage)
   1. [CLI](#41-cli)
   2. [Python Module](#42-python-module)
   3. [Docker](#43-docker)
5. [Architecture](#5-architecture)
6. [Testing](#6-testing)
7. [License](#7-license)

---

## 1. Overview

This package offers the core functionality to extract text from documents using vision LLMs and convert it into Markdown. It is highly configurable by environment variables and its design based on dependency injection, that  allows you to easily swap out components. The package is designed to be used as a library, but it also provides a command-line interface (CLI) for easy local execution.

---

## 2. Features

- **Vision-Language OCR:** Supports Ollama, vLLM and OpenAI (and other OpenAI conform providers). Other LLM providers can be easily integrated.
- **CLI Interface:** Simple local execution via command line or container
- **Highly Configurable:** Use environment variables to configure the OCR
- **Dependency Injection:** Easily swap out components for custom implementations
- **LangChain:** Integrates with LangChain
- **Markdown Output:** Outputs well-formatted Markdown text

---

## 3. Installation

### 3.1 Prerequisites

- **Python:** 3.11+
- **Poetry:** [Install Poetry](https://python-poetry.org/docs/)
- **Docker:** For containerized CLI usage (optional)
- **Ollama:** Follow instructions [here](https://ollama.com) (other LLM providers can be used as well, see [here](#2-features))
- **Langfuse:** Different options for self hosting, see [here](https://langfuse.com/self-hosting) (optional, for observability)

### 3.2 Environment Setup

The package is published on PyPI, so you can install it directly with pip:

```bash
pip install langchain-ocr-lib
```
However, if you want to run the latest version or contribute to the project, you can clone the repository and install it locally.

```bash
git clone https://github.com/a-klos/langchain-ocr.git
cd langchain-ocr/langchain_ocr_lib
poetry install --with dev
```

You can configure the package by setting environment variables. Configuration options are shown in the [`.env.template`](../.env.template) file. 


---

## 4. Usage

Remember that you need to pull the configured LLM model first. With Ollama, you can do this with:
```bash
ollama pull <model_name>
```
For example, to pull the `gemma3:4b-it-q4_K_M` model, run:

```bash
ollama pull gemma3:4b-it-q4_K_M
```

### 4.1 CLI

Run OCR locally from the terminal:

```bash
langchain-ocr <<input_file>> 
```

Supports:
- `.jpg`, `.jpeg`, `.png`, and `.pdf` inputs

### 4.2 Python Module

Use the the library programmatically:

```python
import inject

import configure_di
from langchain_ocr_lib.di_config import configure_di
from langchain_ocr_lib.di_binding_keys.binding_keys import PdfConverterKey
from langchain_ocr_lib.impl.converter.pdf_converter import Pdf2MarkdownConverter


configure_di() #This sets up the dependency injection

class Converter:
    _converter: Pdf2MarkdownConverter = inject.attr(PdfConverterKey)
    def convert(self, filename: str) -> str:
        return self._converter.convert2markdown(filename=filename)

converter = Converter()
markdown = converter.convert("../examples/invoice.pdf") # Adjust the file path as needed
print(markdown)
```

The `configure_di()` function sets up the dependency injection for the library. The dependencies can be easily swapped out or appended with new dependencies. See [../api/src/langchain_ocr/di_config.py](../api/src/langchain_ocr/di_config.py) for more details on how to add new dependencies.

Swapping out the dependencies can be done as follows:

```python
import inject
from inject import Binder

from langchain_ocr_lib.di_config import lib_di_config, PdfConverterKey
from langchain_ocr_lib.impl.converter.pdf_converter import Pdf2MarkdownConverter


class MyPdfConverter(Pdf2MarkdownConverter):
    def convert(self, filename: str) -> None:
        markdown = self.convert2markdown(filename=filename)
        print(markdown)

def _api_specific_config(binder: Binder):
    binder.install(lib_di_config)  # Install all default bindings
    binder.bind(PdfConverterKey, MyPdfConverter())  # Then override PdfConverter

def configure():
    """Configure the dependency injection container."""
    inject.configure(_api_specific_config, allow_override=True, clear=True)

configure()

class Converter:
    _converter: MyPdfConverter = inject.attr(PdfConverterKey)
    def convert(self, filename: str) -> None:
        self._converter.convert(filename=filename)

converter = Converter()
converter.convert("../examples/invoice.pdf") # Adjust the file path as needed
```

### 4.3 Docker

Run OCR via Docker without local Python setup:

```bash
docker build -t ocr -f langchain_ocr_lib/Dockerfile .
docker run --net=host -it --rm -v ./examples:/app/examples:ro ocr examples/invoice.png
```
