"""Module containing the Large Language Model (LLM) type enum class."""

from enum import StrEnum, unique


@unique
class LLMType(StrEnum):
    """Enum class representing different types of Large Language Models (LLMs)."""

    OLLAMA = "ollama"
    OPENAI = "openai"
    VLLM = "vllm"
    TOGETHERAI = "togetherai"
