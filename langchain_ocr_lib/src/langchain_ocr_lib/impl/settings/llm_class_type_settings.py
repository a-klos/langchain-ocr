from pydantic import Field
from pydantic_settings import BaseSettings

from langchain_ocr_lib.impl.llms.llm_type import LLMType


class LlmClassTypeSettings(BaseSettings):
    
    class Config:
        """Config class for reading Fields from env."""

        env_prefix = "RAG_CLASS_TYPE_"
        case_sensitive = False

    llm_type: LLMType = Field(
        default=LLMType.OLLAMA,
    )
