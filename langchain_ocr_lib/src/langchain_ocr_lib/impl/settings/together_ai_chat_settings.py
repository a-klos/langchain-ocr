"""Module contains settings regarding the Together AI API."""

from pydantic import Field
from pydantic_settings import BaseSettings


class TogetherAISettings(BaseSettings):
    """
    Contains settings regarding the Together AI API.

    Attributes
    ----------
    model_name : str
        The Together AI model identifier.
    api_key : str
        The API key for authentication.
    top_p : float
        Total probability mass of tokens to consider at each step.
    temperature : float
        What sampling temperature to use.
    base_url : str
        The base URL for the Together AI API endpoint.
    """

    class Config:
        """Config class for reading fields from environment variables."""

        env_prefix = "TOGETHER_"
        case_sensitive = False

    model_name: str = Field(
        default="",
        description="The Together AI model identifier",
        title="Together AI Model",
    )
    together_api_key: str = Field(default="", description="The API key for authentication")
    top_p: float = Field(
        default=1.0, description="Total probability mass of tokens to consider at each step", title="Top P"
    )
    temperature: float = Field(default=0, description="What sampling temperature to use", title="Temperature")
    together_api_base: str = Field(
        default="https://api.together.xyz/v1/",
        env="API_BASE",
        description="The base URL for the Together AI API endpoint",
    )
