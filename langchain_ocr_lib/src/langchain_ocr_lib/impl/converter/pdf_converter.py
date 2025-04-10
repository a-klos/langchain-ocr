"""Module for converting PDF files to markdown."""

from pdf2image import convert_from_bytes
import io
import base64

from langchain_ocr_lib.converter.converter import File2MarkdownConverter


class Pdf2MarkdownConverter(File2MarkdownConverter):
    """Converts PDF files to markdown format.

    This class provides methods to convert PDF files, either provided as bytes or by filename,
    into markdown format.

    Attributes
    ----------
    _chain : Chain
        The OCR chain used to process images.
    """

    async def aconvert2markdown(self, file: bytes | None = None, filename: str | None = None) -> str:
        """Asynchronously converts a PDF file (either provided as bytes or by filename) into markdown.

        Parameters
        ----------
        file : bytes, optional
            The PDF file as bytes. Defaults to None.
        filename : str, optional
            The path to the PDF file. Defaults to None.

        Returns
        -------
        str
            The markdown representation of the PDF content extracted via OCR.

        Raises
        ------
        ValueError
            If neither `file` nor `filename` is provided.
        ValueError
            If the PDF file is corrupted or the file type is unsupported.
        """
        if file is None and filename is None:
            raise ValueError("No file provided")
        if file is None:
            try:
                with open(filename, "rb") as f:
                    file = f.read()
            except Exception as e:
                raise ValueError("PDF corrupted or unsupported file type") from e
        try:
            images = convert_from_bytes(file)
        except Exception as e:
            raise ValueError("PDF corrupted or unsupported file type") from e

        markdown = ""
        for image in images:
            # Wrap the image in a Document if your chain expects it.
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
            response = await self._chain.ainvoke({"image_data": base64_img})
            markdown += response.content
        return markdown

    def convert2markdown(self, file: bytes | None = None, filename: str | None = None) -> str:
        """Convert a PDF file (either provided as bytes or by filename) into markdown.

        Parameters
        ----------
        file : bytes, optional
            The PDF file as bytes. Defaults to None.
        filename : str, optional
            The path to the PDF file. Defaults to None.

        Returns
        -------
        str
            The markdown representation of the PDF content extracted via OCR.

        Raises
        ------
        ValueError
            If neither `file` nor `filename` is provided.
        ValueError
            If the PDF file is corrupted or the file type is unsupported.
        """
        if file is None and filename is None:
            raise ValueError("No file provided")
        if file is None:
            try:
                with open(filename, "rb") as f:
                    file = f.read()
            except Exception as e:
                raise ValueError("PDF corrupted or unsupported file type") from e

        try:
            images = convert_from_bytes(file)
        except Exception as e:
            raise ValueError("PDF corrupted or unsupported file type") from e

        markdown = ""
        for image in images:
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            base64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
            response = self._chain.invoke({"image_data": base64_img})
            markdown += response.content
        return markdown
