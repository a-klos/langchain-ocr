


from abc import ABC, abstractmethod
from typing import Tuple, Union

from pydantic import StrictBytes, StrictStr

from langchain_ocr.chains.async_chain import AsyncChain


class ConvertFile2Markdown(ABC):
    """
    Abstract base class for the ConvertFile2Markdown class.
    """
    
    def __init__(self, chain: AsyncChain):
        self._chain=chain
    
    @abstractmethod
    def convert2markdown(self, file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]) -> str:
        raise NotImplementedError