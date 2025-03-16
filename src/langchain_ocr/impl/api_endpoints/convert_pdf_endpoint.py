from fastapi import UploadFile
from langchain_core.documents import Document

from langchain_ocr.api_endpoints.convert_base import ConvertFile2Markdown
from langchain_ocr.chains.async_chain import AsyncChain
from pdf2image import convert_from_bytes
import io
import base64

class ConvertPdfEndpoint(ConvertFile2Markdown):
    
    def __init__(self, chain: AsyncChain):
        super().__init__(chain)
    
    async def aconvert2markdown(self, body: UploadFile) -> str:
        file = await body.read()


        if isinstance(file, bytes):
            pdf_bytes = file
        else:
            raise ValueError("Unsupported file type")

        images = convert_from_bytes(pdf_bytes)

        markdown = ""
        for i, image in enumerate(images):
            # Wrap the image in a Document if your chain expects it.
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            image.save(f"page_{i}.png")
            base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
            # doc = Document(page_content=f"data:image/jpeg;base64,{base64_img}", metadata={"page": i})
            response = await self._chain.ainvoke({"image_data": base64_img})
            markdown += response.content
        return markdown
