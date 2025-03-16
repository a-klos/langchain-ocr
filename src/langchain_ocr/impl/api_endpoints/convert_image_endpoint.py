from fastapi import UploadFile
from langchain_core.documents import Document

from langchain_ocr.api_endpoints.convert_base import ConvertFile2Markdown
from langchain_ocr.chains.async_chain import AsyncChain
from pdf2image import convert_from_bytes
import io
import base64
from PIL import Image

class ConvertImageEndpoint(ConvertFile2Markdown):
    
    def __init__(self, chain: AsyncChain):
        super().__init__(chain)
    
    async def aconvert2markdown(self, body: UploadFile) -> str:
        file = await body.read()

        try:
            image = Image.open(io.BytesIO(file))
            
        except Exception as e:
            raise ValueError("Image corrupted or unsupported file type")
        
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        image.save(f"image.png") #
        base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        response = await self._chain.ainvoke({"image_data": base64_img})
        
        return response.content
