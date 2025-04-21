import inject

from langchain_ocr_lib.di_config import configure_di
from langchain_ocr_lib.di_binding_keys.binding_keys import PdfConverterKey
from langchain_ocr_lib.impl.converter.pdf_converter import Pdf2MarkdownConverter


configure_di()  # This sets up the dependency injection


class Converter:
    _converter: Pdf2MarkdownConverter = inject.attr(PdfConverterKey)

    def convert(self, filename: str) -> str:
        return self._converter.convert2markdown(filename=filename)
