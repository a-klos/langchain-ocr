


from abc import ABC, abstractmethod

from fastapi import UploadFile


class ConvertFile2Markdown(ABC):
    """
    Abstract base class for the ConvertFile2Markdown class.
    """
    
    @abstractmethod
    async def aconvert2markdown(self, file: UploadFile) -> str:
        raise NotImplementedError