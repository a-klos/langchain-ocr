# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictBytes, StrictStr
from typing import Any, Tuple, Union
from typing_extensions import Annotated
from langchain_ocr.models.convert_pdf_post400_response import ConvertPdfPost400Response


class BaseOcrApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseOcrApi.subclasses = BaseOcrApi.subclasses + (cls,)
    async def convert_docx_post(
        self,
        file: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The DOCX file to convert.")],
    ) -> str:
        """Accepts a DOCX file and returns its content as Markdown."""
        ...


    async def convert_html_post(
        self,
        file: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The HTML file to convert.")],
    ) -> str:
        """Accepts an HTML file and returns its content as Markdown."""
        ...


    async def convert_pdf_post(
        self,
        file: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The PDF file to convert.")],
    ) -> str:
        """Accepts a PDF file and returns its content as Markdown."""
        ...


    async def convert_pptx_post(
        self,
        file: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The PPTX file to convert.")],
    ) -> str:
        """Accepts a PPTX file and returns its content as Markdown."""
        ...
