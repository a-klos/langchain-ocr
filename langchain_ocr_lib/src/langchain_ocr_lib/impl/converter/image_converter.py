"""Module for converting an image to markdown using a Langchain chain."""

import io
import base64
from PIL import Image
from PIL.ImageFile import ImageFile

from langchain_ocr_lib.converter.converter import File2MarkdownConverter


class Image2MarkdownConverter(File2MarkdownConverter):
    """Converts an image to markdown using a Langchain chain."""

    async def aconvert2markdown(self, file: ImageFile | None = None, filename: str | None = None) -> str:
        """
        Asynchronously converts an image to markdown using a Langchain chain.

        Parameters
        ----------
        file : ImageFile | None, optional
            PIL Image object to convert, by default None
        filename : str | None, optional
            Path to the image file to convert, by default None

        Returns
        -------
        str
            Markdown representation of the image.

        Raises
        ------
        ValueError
            If no file or filename is provided.
        ValueError
            If the file is corrupted or the file type is unsupported.
        """
        if file is None and filename is None:
            raise ValueError("No file provided")
        if file is None:
            try:
                file = Image.open(filename)
            except Exception as e:
                raise ValueError("Image corrupted or unsupported file type, %s" % e)

        buf = io.BytesIO()
        file.save(buf, format="PNG")
        base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        response = await self._chain.ainvoke({"image_data": base64_img})

        return response.content

    def convert2markdown(self, file: ImageFile | None = None, filename: str | None = None) -> str:
        """
        Convert an image to markdown using a Langchain chain.

        Parameters
        ----------
        file : ImageFile | None, optional
            PIL Image object to convert, by default None
        filename : str | None, optional
            Path to the image file to convert, by default None

        Returns
        -------
        str
            Markdown representation of the image.

        Raises
        ------
        ValueError
            If no file or filename is provided.
        ValueError
            If the file is corrupted or the file type is unsupported.
        """
        if file is None and filename is None:
            raise ValueError("No file provided")
        if file is None:
            try:
                file = Image.open(filename)
            except Exception as e:
                raise ValueError("Image corrupted or unsupported file type, %s" % e)

        buf = io.BytesIO()
        file.save(buf, format="PNG")
        base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        response = self._chain.invoke({"image_data": base64_img})

        return response.content
