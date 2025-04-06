"""Module for the implementation of the ConvertImageEndpoint class."""

from fastapi import UploadFile
import inject
import io
from PIL import Image
from langchain_ocr_lib.di_binding_keys.binding_keys import ImageConverterKey
from langchain_ocr_lib.impl.converter.image_converter import Image2MarkdownConverter

from langchain_ocr.api_endpoints.convert_base import ConvertFile2Markdown


class ConvertImageEndpoint(ConvertFile2Markdown):
    """Converts an image to markdown format.

    Attributes
    ----------
    _converter : Image2MarkdownConverter
        An instance of the Image2MarkdownConverter class, injected using the `inject` library.
        This converter is responsible for performing the actual image to markdown conversion.
    """

    _converter: Image2MarkdownConverter = inject.attr(ImageConverterKey)

    async def aconvert2markdown(self, body: UploadFile) -> str:
        """Asynchronously converts an uploaded image to markdown format.

        Parameters
        ----------
        body : UploadFile
            The uploaded image file.

        Returns
        -------
        str
            The markdown representation of the image.

        Raises
        ------
        ValueError
            If the uploaded file is not a valid image or if the conversion fails.
        """
        file = await body.read()

        try:
            image = Image.open(io.BytesIO(file))

        except Exception as e:
            raise ValueError("Image corrupted or unsupported file type: %s" % e)

        return await self._converter.aconvert2markdown(file=image, filename=None)
