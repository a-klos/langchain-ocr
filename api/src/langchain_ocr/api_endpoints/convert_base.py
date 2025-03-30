"""Abstract base class for converting files to markdown format."""
from abc import ABC, abstractmethod

from fastapi import UploadFile


class ConvertFile2Markdown(ABC):
    """Abstract base class for the ConvertFile2Markdown class."""

    @abstractmethod
    async def aconvert2markdown(self, file: UploadFile) -> str:
        """Convert the uploaded file to markdown format.

        Parameters
        ----------
        file : UploadFile
            The file to be converted.

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
