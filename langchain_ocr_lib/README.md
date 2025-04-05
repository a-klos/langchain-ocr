# langchain_ocr_lib

**langchain_ocr_lib** is the OCR processing engine behind LangChain-OCR. It provides a modular, vision-LLM-powered pipeline to convert image and PDF documents into clean Markdown. Designed for direct CLI usage or integration into larger LangChain-based applications.

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

This package offers the core functionality to extract text from visual documents using LLMs and convert it into Markdown. It includes file loading, OCR inference, Markdown postprocessing, and environment-configurable components — all in a single pipeline.

---

## 2. Features

- **Vision-Language OCR:** Support for OpenAI, HuggingFace, and custom extractors
- **CLI Interface:** Simple local execution via command line or container
- **Pluggable Architecture:** Swap extractors, loaders, and formatters easily
- **LangChain Ready:** Integrates with LangChain agents or workflows
- **Markdown Output:** Outputs well-formatted Markdown text, not raw OCR

---

## 3. Installation

### 3.1 Prerequisites

- **Python:** 3.11+
- **Poetry:** [Install Poetry](https://python-poetry.org/docs/)
- (Optional) **Docker:** For containerized CLI usage

### 3.2 Environment Setup

Clone and install dependencies with Poetry:

```bash
git clone https://github.com/a-klos/langchain-ocr.git
cd langchain-ocr
poetry install
```

---

## 4. Usage

### 4.1 CLI

Run OCR locally from the terminal:

```bash
poetry run python -m langchain_ocr_lib.cli \
  --input path/to/input.jpg \
  --output path/to/output.md
```

Supports:
- `.jpg`, `.jpeg`, `.png`, and `.pdf` inputs

### 4.2 Python Module

Use the pipeline programmatically:

```python
from langchain_ocr_lib.pipeline import OCRPipeline

ocr = OCRPipeline()
markdown = ocr.run("invoice.png")
print(markdown)
```

### 4.3 Docker

Run OCR via Docker without local Python setup:

```bash
docker build -t langchain-ocr-cli -f langchain_ocr_lib/Dockerfile .
docker run --rm -v $(pwd):/data langchain-ocr-cli \
  --input /data/samples/invoice.png \
  --output /data/output/invoice.md
```
