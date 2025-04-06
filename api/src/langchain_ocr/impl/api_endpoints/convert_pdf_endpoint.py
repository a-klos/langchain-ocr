"""Module for the ConvertPdfEndpoint class."""

from fastapi import UploadFile
import inject
from langchain_ocr_lib.di_binding_keys.binding_keys import PdfConverterKey
from langchain_ocr_lib.impl.converter.pdf_converter import Pdf2MarkdownConverter

from langchain_ocr.api_endpoints.convert_base import ConvertFile2Markdown


class ConvertPdfEndpoint(ConvertFile2Markdown):
    """Converts PDF files to Markdown format using a Pdf2MarkdownConverter.

    Attributes
    ----------
    _converter : Pdf2MarkdownConverter
        An injected dependency of Pdf2MarkdownConverter used for the conversion.
    """

    _converter: Pdf2MarkdownConverter = inject.attr(PdfConverterKey)

    async def aconvert2markdown(self, body: UploadFile) -> str:
        """Asynchronously converts a PDF file to Markdown format.

        Parameters
        ----------
        body : UploadFile
            The uploaded PDF file.

        Returns
        -------
        str
            The Markdown representation of the PDF.

        Raises
        ------
        ValueError
            If the uploaded file is not of a supported type.
        """
        file = await body.read()
        if isinstance(file, bytes):
            pdf_bytes = file
        else:
            raise ValueError("Unsupported file type")

        return await self._converter.aconvert2markdown(file=pdf_bytes, filename=None)
