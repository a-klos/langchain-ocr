from fastapi import UploadFile
import inject
import io
from PIL import Image
from langchain_ocr_lib.impl.converter.image_converter import Image2MarkdownConverter

from langchain_ocr.api_endpoints.convert_base import ConvertFile2Markdown


class ConvertImageEndpoint(ConvertFile2Markdown):
    _converter: Image2MarkdownConverter = inject.attr("ImageConverter")    
    async def aconvert2markdown(self, body: UploadFile) -> str:
        file = await body.read()

        try:
            image = Image.open(io.BytesIO(file))
            
        except Exception as e:
            raise ValueError("Image corrupted or unsupported file type")
        
        markdown = await self._converter.aconvert2markdown(image=image, filename=None)
        
        return markdown
