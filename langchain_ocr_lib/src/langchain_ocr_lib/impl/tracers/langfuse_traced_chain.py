"""Module for the LangfuseTraceChain class."""

from typing import Optional

import inject
from langchain_core.runnables import RunnableConfig
from langfuse.callback import CallbackHandler

from langchain_ocr_lib.impl.settings.langfuse_settings import LangfuseSettings
from langchain_ocr_lib.tracers.traced_chain import TracedChain
from langchain_ocr_lib.di_config import OcrChainKey


class LangfuseTracedChain(TracedChain):
    """A class to trace the execution of a Runnable using Langfuse.

    This class wraps an inner Runnable and adds tracing capabilities using the Langfuse tracer.
    It allows for the configuration of the tracer through the provided settings.

    Attributes
    ----------
    CONFIG_CALLBACK_KEY : str
        The key used to store callbacks in the configuration.
    """

    CONFIG_CALLBACK_KEY = "callbacks"
    _inner_chain = inject.attr(OcrChainKey)

    def __init__(self, settings: LangfuseSettings):
        super().__init__()
        self._settings = settings

    def _add_tracing_callback(self, session_id: str, config: Optional[RunnableConfig]) -> RunnableConfig:
        handler = CallbackHandler(
            public_key=self._settings.public_key,
            secret_key=self._settings.secret_key,
            host=self._settings.host,
            session_id=session_id,
        )
        if not config:
            return RunnableConfig(callbacks=[handler])

        current_callbacks = config.get(self.CONFIG_CALLBACK_KEY, [])
        config[self.CONFIG_CALLBACK_KEY] = (current_callbacks if current_callbacks else []) + [handler]
        return config
