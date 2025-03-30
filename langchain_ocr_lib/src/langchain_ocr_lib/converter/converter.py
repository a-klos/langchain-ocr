"""Module for the File2MarkdownConverter class."""

from abc import ABC, abstractmethod
from fastapi import UploadFile
import inject


class File2MarkdownConverter(ABC):
    """Abstract base class for the File2MarkdownConverter class."""

    _chain = inject.attr("LangfuseTracedChain")

    @abstractmethod
    async def aconvert2markdown(self, file: UploadFile) -> str:
        """Asynchronously convert file to markdown format.

        Parameters
        ----------
        file : UploadFile
            The file to convert.

        Returns
        -------
        str
            The markdown representation of the file.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def convert2markdown(self, file: UploadFile) -> str:
        """Convert file to markdown format.

        Parameters
        ----------
        file : UploadFile
            The file to convert.

        Returns
        -------
        str
            The markdown representation of the file.

        Raises
        ------
        NotImplementedError
            If the method is not implemented.
        """
        raise NotImplementedError
