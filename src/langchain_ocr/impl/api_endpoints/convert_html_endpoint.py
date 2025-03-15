from abc import ABC, abstractmethod
from typing import Tuple, Union

from pydantic import StrictBytes, StrictStr
from langchain_core.language_models.llms import LLM

from langchain_ocr.api_endpoints.convert_base import ConvertFile2Markdown

class ConvertHtmlEndpoint(ConvertFile2Markdown):

    def __init__(self, llm:LLM):
        super().__init__(llm)
    
    def convert2markdown(self, file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]) -> str:
        raise NotImplementedError