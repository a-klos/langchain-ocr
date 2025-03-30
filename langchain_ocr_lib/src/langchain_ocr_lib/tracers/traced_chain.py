"""Module for the TracedGraph class."""

import uuid
from abc import ABC, abstractmethod
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig, ensure_config

from langchain_ocr_lib.chains.chain import Chain

RunnableInput = Any
RunnableOutput = Any


class TracedChain(Chain[RunnableInput, RunnableOutput], ABC):
    """A class to represent a traced graph in an asynchronous chain.

    This class is designed to wrap around an inner Runnable chain and add tracing capabilities to it.
    It provides methods to asynchronously invoke the chain with tracing and to manage session IDs and tracing callbacks.

    Attributes
    ----------
    SESSION_ID_KEY : str
        The key used to store the session ID in the metadata.
    METADATA_KEY : str
        The key used to store metadata.
    """

    SESSION_ID_KEY = "session_id"
    METADATA_KEY = "metadata"

    async def ainvoke(
        self, chain_input: RunnableInput, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> RunnableOutput:
        """
        Asynchronously invoke the chain with the given input and configuration.

        Parameters
        ----------
        chain_input : RunnableInput
            The input to be processed by the chain.
        config : Optional[RunnableConfig], optional
            Configuration for the chain execution (default None).
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        RunnableOutput
            The output produced by the chain after processing the input.

        """
        config = ensure_config(config)
        session_id = self._get_session_id(config)
        config_with_tracing = self._add_tracing_callback(session_id, config)
        return await self._inner_chain.ainvoke(chain_input, config=config_with_tracing)

    def invoke(
        self, chain_input: RunnableInput, config: Optional[RunnableConfig] = None, **kwargs: Any
    ) -> RunnableOutput:
        """
        Invoke the chain with the given input and configuration.

        Parameters
        ----------
        chain_input : RunnableInput
            The input to be processed by the chain.
        config : Optional[RunnableConfig], optional
            Configuration for the chain execution (default None).
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        RunnableOutput
            The output produced by the chain after processing the input.
        """
        config = ensure_config(config)
        session_id = self._get_session_id(config)
        config_with_tracing = self._add_tracing_callback(session_id, config)
        return self._inner_chain.invoke(chain_input, config=config_with_tracing)

    @abstractmethod
    def _add_tracing_callback(self, session_id: str, config: Optional[RunnableConfig]) -> RunnableConfig:
        ...

    def _get_session_id(self, config: Optional[RunnableConfig]) -> str:
        return config.get(self.METADATA_KEY, {}).get(self.SESSION_ID_KEY, str(uuid.uuid4()))
