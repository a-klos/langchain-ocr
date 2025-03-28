from fastapi import UploadFile
import io
import base64
from PIL import Image
from PIL.ImageFile import ImageFile

from langchain_ocr_lib.converter.converter import File2MarkdownConverter


class Image2MarkdownConverter(File2MarkdownConverter):
   
    async def aconvert2markdown(self, image: ImageFile|None, filename:str|None) -> str:
        if image is None and filename is None:
            raise ValueError("No file provided")
        elif image is None:
            try:
                image = Image.open(filename)
            except Exception as e:
                raise ValueError("Image corrupted or unsupported file type")
        
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        response = await self._chain.ainvoke({"image_data": base64_img})
        
        return response.content
    
    def convert2markdown_sync(self, image: ImageFile | None, filename: str | None) -> str:
        if image is None and filename is None:
            raise ValueError("No file provided")
        elif image is None:
            try:
                image = Image.open(filename)
            except Exception as e:
                raise ValueError("Image corrupted or unsupported file type")
        
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        response = self._chain.invoke({"image_data": base64_img})
        
        return response.content
    
    #  async def aconvert2markdown(self, body: UploadFile) -> str:
    #     file = await body.read()

    #     try:
    #         image = Image.open(io.BytesIO(file))
            
    #     except Exception as e:
    #         raise ValueError("Image corrupted or unsupported file type")
        
    #     buf = io.BytesIO()
    #     image.save(buf, format="PNG")
    #     base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
    #     response = await self._chain.ainvoke({"image_data": base64_img})
        
    #     return response.content
    
    def convert2markdown(self, body: UploadFile) -> str: #TODO: test this
        file = body.file.read()

        try:
            image = Image.open(io.BytesIO(file))
        except Exception as e:
            raise ValueError("Image corrupted or unsupported file type")

        buf = io.BytesIO()
        image.save(buf, format="PNG")
        base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        response = self._chain.invoke({"image_data": base64_img})

        return response.content
    

