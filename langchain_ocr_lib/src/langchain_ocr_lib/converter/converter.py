"""Module for the File2MarkdownConverter class."""

from abc import ABC, abstractmethod
import inject

from langchain_ocr_lib.di_binding_keys.binding_keys import LangfuseTracedChainKey


class File2MarkdownConverter(ABC):
    """Abstract base class for the File2MarkdownConverter class."""

    _chain = inject.attr(LangfuseTracedChainKey)

    @abstractmethod
    async def aconvert2markdown(self, file: bytes) -> str:
        """Asynchronously convert file to markdown format.

        Parameters
        ----------
        file : bytes
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
    def convert2markdown(self, file: bytes) -> str:
        """Convert file to markdown format.

        Parameters
        ----------
        file : bytes
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
