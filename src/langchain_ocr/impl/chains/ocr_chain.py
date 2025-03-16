"""Module for LLM answer generation chain."""

from typing import Any, Optional

from langchain_core.documents import Document
from langchain_core.runnables import Runnable, RunnableConfig, RunnablePassthrough
from langchain_core.runnables.utils import Input

from langchain_ocr.chains.async_chain import AsyncChain
from langchain_ocr.impl.langfuse_manager.langfuse_manager import LangfuseManager

RunnableInput = Input #TODO: adjust properly
RunnableOutput = str


class OcrChain(AsyncChain[RunnableInput, RunnableOutput]):
    """Base class for LLM answer generation chain."""

    def __init__(self, langfuse_manager: LangfuseManager):
        """Initialize the AnswerGenerationChain.

        Parameters
        ----------
        langfuse_manager : LangfuseManager
            Manager instance for handling Langfuse operations and monitoring
        """
        self._langfuse_manager = langfuse_manager



    async def ainvoke(
        self, chain_input: RunnableInput, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> RunnableOutput:
        """
        Asynchronously invokes the chain with given input.

        Parameters
        ----------
        chain_input : RunnableInput
            The input to be processed by the chain.
        chain_config : Optional[RunnableConfig]
            Configuration for the chain execution (default None).
        **kwargs : Any
            Additional keyword arguments passed to the chain.

        Returns
        -------
        RunnableOutput
            The output generated by the chain.

        Raises
        ------
        ChainError
            If an error occurs during chain execution.
        """
        return await self._create_chain().ainvoke(chain_input, config=config)

    def _create_chain(self) -> Runnable:
        return (
            self._langfuse_manager.get_base_prompt(self.__class__.__name__)
            | self._langfuse_manager.get_base_llm(self.__class__.__name__)
        )
