from fastapi import UploadFile
import inject
from pdf2image import convert_from_bytes
import io
import base64

from langchain_ocr_lib.converter.converter import File2MarkdownConverter


class Pdf2MarkdownConverter(File2MarkdownConverter):
    
    async def aconvert2markdown(self, pdf_bytes:bytes|None=None, filename:str|None=None) -> str:
        if pdf_bytes is None and filename is None:
            raise ValueError("No file provided")
        elif pdf_bytes is None:
            try:
                with open(filename, "rb") as f:
                    pdf_bytes = f.read()
            except Exception as e:
                raise ValueError("PDF corrupted or unsupported file type")

        images = convert_from_bytes(pdf_bytes)

        markdown = ""
        for i, image in enumerate(images):
            # Wrap the image in a Document if your chain expects it.
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
            response = await self._chain.ainvoke({"image_data": base64_img})
            markdown += response.content
        return markdown

    def convert2markdown(self, pdf_bytes: bytes | None=None, filename: str | None=None) -> str:
        if pdf_bytes is None and filename is None:
            raise ValueError("No file provided")
        elif pdf_bytes is None:
            try:
                with open(filename, "rb") as f:
                    pdf_bytes = f.read()
            except Exception as e:
                raise ValueError("PDF corrupted or unsupported file type") from e

        images = convert_from_bytes(pdf_bytes)

        markdown = ""
        for i, image in enumerate(images):
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
            response = self._chain.invoke({"image_data": base64_img})
            markdown += response.content
        return markdown
