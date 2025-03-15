"""Module for the implementation of the RagApi class."""

import logging
from asyncio import run
from threading import Thread
from typing import Tuple, Union
from pydantic import StrictBytes, StrictStr
from typing_extensions import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request, UploadFile

from langchain_ocr.api_endpoints.convert_base import ConvertFile2Markdown
from langchain_ocr.apis.ocr_api_base import BaseOcrApi
from langchain_ocr.dependency_container import DependencyContainer


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
    
    @inject
    async def convert_pdf_post(
        self,
        body: UploadFile,
        request: Request,
        convert_pdf_endpoint: ConvertFile2Markdown = Depends(Provide[DependencyContainer.convert_pdf_endpoint]),
    ) -> str:
        return convert_pdf_endpoint.convert2markdown(body)

