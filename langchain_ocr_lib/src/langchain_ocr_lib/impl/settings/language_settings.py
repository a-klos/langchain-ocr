"""Module containing the LanguageSettings class."""

from pydantic import Field
from pydantic_settings import BaseSettings


class LanguageSettings(BaseSettings):
    """
    Contains settings regarding the language used for OCR.

    Attributes
    ----------
    language : str
        The language to use for OCR.
    """

    class Config:
        """Config class for reading fields from environment variables."""

        env_prefix = "OCR_"
        case_sensitive = False

    language: str = Field(
        default="en", description="The language in iso 639-1 format, e.g. 'en' for English, 'de' for German, etc."
    )
