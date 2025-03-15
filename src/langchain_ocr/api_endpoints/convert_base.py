


from abc import ABC, abstractmethod
from typing import Tuple, Union

from pydantic import StrictBytes, StrictStr
from langchain_core.language_models.llms import LLM


class ConvertFile2Markdown(ABC):
    """
    Abstract base class for the ConvertFile2Markdown class.
    """
    
    def __init__(self, llm:LLM):
        self._llm = llm
    
    @abstractmethod
    def convert2markdown(self, file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]) -> str:
        raise NotImplementedError