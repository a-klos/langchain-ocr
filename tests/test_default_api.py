# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictBytes, StrictStr  # noqa: F401
from typing import Tuple, Union  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from langchain_ocr.models.convert_pdf_post400_response import ConvertPdfPost400Response  # noqa: F401


def test_convert_docx_post(client: TestClient):
    """Test case for convert_docx_post

    Convert DOCX to Markdown
    """

    headers = {
    }
    data = {
        "file": '/path/to/file'
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/convert/docx",
    #    headers=headers,
    #    data=data,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_convert_html_post(client: TestClient):
    """Test case for convert_html_post

    Convert HTML to Markdown
    """

    headers = {
    }
    data = {
        "file": '/path/to/file'
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/convert/html",
    #    headers=headers,
    #    data=data,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_convert_pdf_post(client: TestClient):
    """Test case for convert_pdf_post

    Convert PDF to Markdown
    """

    headers = {
    }
    data = {
        "file": '/path/to/file'
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/convert/pdf",
    #    headers=headers,
    #    data=data,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_convert_pptx_post(client: TestClient):
    """Test case for convert_pptx_post

    Convert PPTX to Markdown
    """

    headers = {
    }
    data = {
        "file": '/path/to/file'
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/convert/pptx",
    #    headers=headers,
    #    data=data,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

