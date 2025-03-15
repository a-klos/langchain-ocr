from abc import ABC, abstractmethod
from typing import Tuple, Union

from pydantic import StrictBytes, StrictStr
from langchain_core.documents import Document

from langchain_ocr.api_endpoints.convert_base import ConvertFile2Markdown
from langchain_ocr.chains.async_chain import AsyncChain
from pdf2image import convert_from_bytes

class ConvertPdfEndpoint(ConvertFile2Markdown):
    
    def __init__(self, chain: AsyncChain):
        super().__init__(chain)
    
    def convert2markdown(self, file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]) -> str:
        
        if isinstance(file, tuple):
            pdf_bytes = file[1]
        elif isinstance(file, bytes):
            pdf_bytes = file
        elif isinstance(file, str):
            with open(file, "rb") as f:
                pdf_bytes = f.read()
        else:
            raise ValueError("Unsupported file type")

        images = convert_from_bytes(pdf_bytes)

        markdown = ""
        for i, image in enumerate(images):
            # Wrap the image in a Document if your chain expects it.
            doc = Document(page_content=image, metadata={"page": i})
            response = self._chain.ainvoke(doc)
            markdown += response
        return markdown
