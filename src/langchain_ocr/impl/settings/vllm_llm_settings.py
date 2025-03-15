"""Module contains settings regarding the vLLM."""

from pydantic import Field
from pydantic_settings import BaseSettings


class VllmSettings(BaseSettings):
    """
    Contains settings regarding the vLLM.

    Attributes
    ----------
    model : str
        The model identifier.
    base_url : str
        The base URL for the model serving endpoint.
    api_key : str
        The API key for authentication.
    top_p : float
        Total probability mass of tokens to consider at each step.
    temperature : float
        What sampling temperature to use.
    """

    class Config:
        """Config class for reading Fields from env."""

        env_prefix = "VLLM_"
        case_sensitive = False

    model: str 
    base_url: str
    api_key: str

    top_p: float = Field(default=0.1, title="LLM Top P")
    temperature: float = Field(default=0, title="LLM Temperature")
