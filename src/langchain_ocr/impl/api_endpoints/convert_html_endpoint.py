from abc import ABC, abstractmethod
from typing import Tuple, Union

from pydantic import StrictBytes, StrictStr

from langchain_ocr.api_endpoints.convert_base import ConvertFile2Markdown
from langchain_ocr.chains.async_chain import AsyncChain

class ConvertHtmlEndpoint(ConvertFile2Markdown):

    def __init__(self, chain: AsyncChain):
        super().__init__(chain)
    
    def convert2markdown(self, file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]) -> str:
        raise NotImplementedError