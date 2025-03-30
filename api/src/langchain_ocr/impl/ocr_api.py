"""Module for the implementation of the RagApi class."""

import logging

from fastapi import Request, UploadFile
import inject

from langchain_ocr.impl.api_endpoints.convert_pdf_endpoint import ConvertPdfEndpoint
from langchain_ocr.impl.api_endpoints.convert_image_endpoint import ConvertImageEndpoint
from langchain_ocr.apis.ocr_api_base import BaseOcrApi


logger = logging.getLogger(__name__)


class OcrApi(BaseOcrApi):
    """
    RagApi class for handling various endpoints of the RAG API.

    This class provides asynchronous methods to handle chat requests, evaluate the RAG,
    remove information pieces, and upload information pieces. It manages background threads
    for evaluation tasks and uses dependency injection for its dependencies.
    """

    def __init__(self):
        """Initialize the instance of the class."""
        super().__init__()
        self._background_threads = []

    async def convert_image_post(
        self,
        body: UploadFile,
        request: Request,
    ) -> str:
        """
        Convert an image file to Markdown.

        Parameters
        ----------
        body : UploadFile
            The uploaded image file.
        request : Request
            The incoming request.

        Returns
        -------
        str
            The converted Markdown content.
        """
        logger.info("Received a request to convert the following PDF file to Markdown: %s", body.filename)
        convert_image_endpoint = inject.instance(ConvertImageEndpoint)
        return await convert_image_endpoint.aconvert2markdown(body)

    async def convert_pdf_post(
        self,
        body: UploadFile,
        request: Request,
    ) -> str:
        """
        Convert a PDF file to Markdown.

        Parameters
        ----------
        body : UploadFile
            The uploaded PDF file.
        request : Request
            The incoming request.

        Returns
        -------
        str
            The converted Markdown content.
        """
        logger.info("Received a request to convert the following PDF file to Markdown: %s", body.filename)
        convert_pdf_endpoint = inject.instance(ConvertPdfEndpoint)
        return await convert_pdf_endpoint.aconvert2markdown(body)
