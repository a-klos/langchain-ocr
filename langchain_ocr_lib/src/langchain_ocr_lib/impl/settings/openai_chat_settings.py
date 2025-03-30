"""Module contains settings regarding the OpenAI API."""

from pydantic import Field
from pydantic_settings import BaseSettings


class OpenAISettings(BaseSettings):
    """
    Contains settings regarding the OpenAI API.

    Attributes
    ----------
    model : str
        The model identifier.
    api_key : str
        The API key for authentication.
    top_p : float
        Total probability mass of tokens to consider at each step.
    temperature : float
        What sampling temperature to use.
    vision_capable : bool
        Flag to enable a vision capable model.
    """

    class Config:
        """Config class for reading fields from environment variables."""

        env_prefix = "OPENAI_"
        case_sensitive = False

    model: str = Field(default="gpt-4o-mini-search-preview-2025-03-11", description="The model identifier")
    api_key: str = Field(default="", description="The API key for authentication")
    top_p: float = Field(default=1.0, description="Total probability mass of tokens to consider at each step")
    temperature: float = Field(default=0.7, description="What sampling temperature to use")
    vision_capable: bool = Field(default=False, description="Enable a vision capable model")
