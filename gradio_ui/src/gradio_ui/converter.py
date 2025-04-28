"""Module for converting PDF files to Markdown format using a converter class."""

import inject

from langchain_ocr_lib.di_config import configure_di
from langchain_ocr_lib.di_binding_keys.binding_keys import PdfConverterKey
from langchain_ocr_lib.impl.converter.pdf_converter import Pdf2MarkdownConverter


configure_di()  # This sets up the dependency injection


class Converter:
    """Class to convert PDF files to Markdown format."""

    _converter: Pdf2MarkdownConverter = inject.attr(PdfConverterKey)

    def convert(self, filename: str) -> str:
        """
        Convert a PDF file to Markdown format.

        Parameters
        ----------
        filename : str
            Path to the PDF file.

        Returns
        -------
        str
            Markdown formatted content.
        """
        return self._converter.convert2markdown(filename=filename)
