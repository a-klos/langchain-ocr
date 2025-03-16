# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from fastapi import Request, UploadFile
from pydantic import Field, StrictBytes, StrictStr
from typing import Any, Tuple, Union
from typing_extensions import Annotated
from langchain_ocr.models.convert_pdf_post400_response import ConvertPdfPost400Response


class BaseOcrApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseOcrApi.subclasses = BaseOcrApi.subclasses + (cls,)
    async def convert_image_post(
        self,
        body: UploadFile,
        request: Request,
    ) -> str:
        """Accepts an image file (JPEG and PNG) and returns its content as Markdown."""
        ...


    async def convert_pdf_post(
        self,
        body: UploadFile,
        request: Request,
    ) -> str:
        """Accepts a PDF file and returns its content as Markdown."""
        ...
