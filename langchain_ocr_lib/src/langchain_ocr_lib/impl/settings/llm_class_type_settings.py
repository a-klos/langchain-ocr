"""Module for the LLM class type settings."""

from pydantic import Field
from pydantic_settings import BaseSettings

from langchain_ocr_lib.impl.llms.llm_type import LLMType


class LlmClassTypeSettings(BaseSettings):
    """Settings for the LLM class type.

    Attributes
    ----------
    llm_type : LLMType
        The type of LLM to use. Defaults to LLMType.OLLAMA.

    """

    class Config:
        """Config class for reading Fields from env."""

        env_prefix = "RAG_CLASS_TYPE_"
        case_sensitive = False

    llm_type: LLMType = Field(
        default=LLMType.OLLAMA,
    )
