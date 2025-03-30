import logging
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import UploadFile, Request

# Fix the imports to use the full module paths
from src.langchain_ocr.impl.ocr_api import OcrApi
from src.langchain_ocr.impl.api_endpoints.convert_pdf_endpoint import ConvertPdfEndpoint
from src.langchain_ocr.impl.api_endpoints.convert_image_endpoint import ConvertImageEndpoint

"""Tests for the OcrApi class."""


@pytest.fixture
def mock_convert_image_endpoint():
    endpoint = MagicMock()
    endpoint.aconvert2markdown = AsyncMock(return_value="Markdown from image")
    return endpoint


@pytest.fixture
def mock_convert_pdf_endpoint():
    endpoint = MagicMock()
    endpoint.aconvert2markdown = AsyncMock(return_value="Markdown from PDF")
    return endpoint


@pytest.fixture
def mock_inject(mock_convert_image_endpoint, mock_convert_pdf_endpoint):
    # Fix the patch path to target where inject is used
    with patch("src.langchain_ocr.impl.ocr_api.inject.instance") as mock_instance:

        def side_effect(arg):
            if arg is ConvertImageEndpoint:
                return mock_convert_image_endpoint
            elif arg is ConvertPdfEndpoint:
                return mock_convert_pdf_endpoint

        mock_instance.side_effect = side_effect
        yield mock_instance


@pytest.fixture
def api(mock_convert_image_endpoint, mock_convert_pdf_endpoint):
    with patch("src.langchain_ocr.impl.ocr_api.inject.instance") as mock_instance:
        # Set up the mock to return our endpoints
        mock_instance.side_effect = (
            lambda cls: mock_convert_image_endpoint if cls is ConvertImageEndpoint else mock_convert_pdf_endpoint
        )

        # Create the API instance
        api_instance = OcrApi()

        yield api_instance


@pytest.fixture
def mock_request():
    return MagicMock(spec=Request)


@pytest.fixture
def mock_upload_file():
    file = MagicMock(spec=UploadFile)
    file.filename = "test_file.jpg"
    return file


@pytest.mark.asyncio
async def test_convert_image_post(api, mock_upload_file, mock_request, mock_convert_image_endpoint):
    # Call the method
    result = await api.convert_image_post(mock_upload_file, mock_request)

    # Check the results
    mock_convert_image_endpoint.aconvert2markdown.assert_called_once_with(mock_upload_file)
    assert result == "Markdown from image"


@pytest.mark.asyncio
async def test_convert_pdf_post(api, mock_upload_file, mock_request, mock_convert_pdf_endpoint):
    # Update filename for PDF test
    mock_upload_file.filename = "test_file.pdf"

    # Call the method
    result = await api.convert_pdf_post(mock_upload_file, mock_request)

    # Check the results
    mock_convert_pdf_endpoint.aconvert2markdown.assert_called_once_with(mock_upload_file)
    assert result == "Markdown from PDF"
