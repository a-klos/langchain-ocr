from fastapi import UploadFile
import inject
from langchain_ocr_lib.impl.converter.pdf_converter import Pdf2MarkdownConverter

from langchain_ocr.api_endpoints.convert_base import ConvertFile2Markdown

class ConvertPdfEndpoint(ConvertFile2Markdown):
    _converter: Pdf2MarkdownConverter = inject.attr("PdfConverter")
    
    async def aconvert2markdown(self, body: UploadFile) -> str:
        file = await body.read()
        if isinstance(file, bytes):
            pdf_bytes = file
        else:
            raise ValueError("Unsupported file type")
    
        # Pass the filename directly to the converter
        markdown = await self._converter.aconvert2markdown(pdf_bytes=pdf_bytes, filename=None)
    
        return markdown
