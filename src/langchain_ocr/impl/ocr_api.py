"""Module for the implementation of the RagApi class."""

import logging
from asyncio import run
from threading import Thread
from typing import Tuple, Union
from pydantic import StrictBytes, StrictStr
from typing_extensions import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from langchain_ocr.impl.api_endpoints.convert_docx_endpoint import ConvertDocxEndpoint
from langchain_ocr.impl.api_endpoints.convert_html_endpoint import ConvertHtmlEndpoint
from langchain_ocr.impl.api_endpoints.convert_pdf_endpoint import ConvertPdfEndpoint
from langchain_ocr.impl.api_endpoints.convert_pptx_endpoint import ConvertPptxEndpoint
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
    async def convert_docx_post(
        self,
        file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
        convert_docx_endpoint: ConvertDocxEndpoint = Depends(Provide[DependencyContainer.chat_endpoint]),
    ) -> str:
        return ""
        
    @inject
    async def convert_html_post(
        self,
        file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
        convert_html_endpoint: ConvertHtmlEndpoint = Depends(Provide[DependencyContainer.chat_endpoint]),
    ) -> str:
        return ""
    
    @inject
    async def convert_pdf_post(
        self,
        file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
        convert_pdf_endpoint: ConvertPdfEndpoint = Depends(Provide[DependencyContainer.chat_endpoint]),
    ) -> str:
        return ""
    
    @inject
    async def convert_pptx_post(
        self,
        file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
        convert_pptx_endpoint: ConvertPptxEndpoint = Depends(Provide[DependencyContainer.chat_endpoint]),
    ) -> str:
        return ""
        
    
