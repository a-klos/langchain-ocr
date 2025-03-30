from abc import ABC, abstractmethod
from typing import Tuple, Union
from fastapi import UploadFile
import inject


class File2MarkdownConverter(ABC):
    """
    Abstract base class for the File2MarkdownConverter class.
    """

    _chain = inject.attr("LangfuseTracedChain")

    @abstractmethod
    async def aconvert2markdown(self, file: UploadFile) -> str:
        raise NotImplementedError

    @abstractmethod
    def convert2markdown(self, file: UploadFile) -> str:
        raise NotImplementedError
