# spell-checker: disable
"""Module for managing Langfuse prompts and Langfuse Language Models (LLMs)."""
import logging
from typing import Optional
import inject
import json

from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models.llms import LLM
from langfuse.api.resources.commons.errors.not_found_error import NotFoundError
from langfuse.model import ChatPromptClient

from langchain_ocr_lib.di_binding_keys.binding_keys import LangfuseClientKey, LargeLanguageModelKey


logger = logging.getLogger(__name__)


class LangfuseManager:
    """Manage prompts using Langfuse and a Large Language Model (LLM).

    Attributes
    ----------
    API_KEY_FILTER : str
        A filter string used to exclude the API key from configurations.
    """

    API_KEY_FILTER: str = "api_key"
    _llm = inject.attr(LargeLanguageModelKey)
    _langfuse = inject.attr(LangfuseClientKey)

    def __init__(
        self,
        managed_prompts: dict[str, str],
        enabled: bool = True,
    ):
        self._managed_prompts = managed_prompts
        self._enabled = enabled

    def get_langfuse_prompt(self, base_prompt_name: str) -> Optional[ChatPromptClient]:
        """
        Retrieve the prompt from Langfuse Prompt Management.

        Parameters
        ----------
        base_prompt_name : str
            The name of the base prompt to retrieve.

        Returns
        -------
        Optional[TextPromptClient]
            The Langfuse prompt template if found, otherwise None.

        Raises
        ------
        NotFoundError
            If the prompt is not found in Langfuse, a new prompt is created.
        Exception
            If an error occurs while retrieving the prompt template from Langfuse.
        """
        if not self._enabled:
            logger.info("Langfuse is not enabled. Using fallback prompt.")
            return None
        try:
            langfuse_prompt = self._langfuse.get_prompt(base_prompt_name)
        except NotFoundError:
            logger.info("Prompt not found in LangFuse. Creating new.")
            llm_configurable_configs = {
                config.id: config.default for config in self._llm.config_specs if self.API_KEY_FILTER not in config.id
            }
            self._langfuse.create_prompt(
                name=base_prompt_name,
                prompt=self._managed_prompts[base_prompt_name],
                config=llm_configurable_configs,
                labels=["production"],
                type="chat",
            )
            langfuse_prompt = self._langfuse.get_prompt(base_prompt_name)
        except Exception as error:
            logger.error(f"Error occurred while getting prompt template from langfuse. Error:\n{error}")
        return langfuse_prompt

    def get_base_llm(self, name: str) -> LLM:
        """
        Get the Langfuse prompt, the configuration as well as Large Language Model (LLM).

        Parameters
        ----------
        name : str
            The name of the Langfuse prompt to retrieve the configuration for.

        Returns
        -------
        LLM
            The base Large Language Model. If the Langfuse prompt is not found,
            returns the LLM with a fallback configuration.
        """
        if not self._enabled:
            logger.info("Langfuse is not enabled. Using fallback LLM.")
            return self._llm
        langfuse_prompt = self.get_langfuse_prompt(name)
        if not langfuse_prompt:
            logger.warning("Could not retrieve prompt template from langfuse. Using fallback LLM.")
            return self._llm

        return self._llm.with_config({"configurable": langfuse_prompt.config})

    def get_base_prompt(self, name: str) -> ChatPromptTemplate:
        """
        Retrieve the base prompt from Langfuse Prompt Management.

        Parameters
        ----------
        name : str
            The name of the prompt to retrieve.

        Returns
        -------
        PromptTemplate
            The base prompt template.

        Notes
        -----
        If the prompt cannot be retrieved from Langfuse, a fallback value is used.
        """
        langfuse_prompt = self.get_langfuse_prompt(name)
        if not langfuse_prompt:
            if self._enabled:
                logger.warning("Could not retrieve prompt template from langfuse. Using fallback value.")
            fallback = self._managed_prompts[name]
            if isinstance(fallback, ChatPromptTemplate):
                return fallback
            if (
                isinstance(fallback, list)
                and len(fallback) > 0
                and isinstance(fallback[0], dict)
                and "content" in fallback[0]
            ):
                image_payload = [{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,{image_data}"}}]
                return ChatPromptTemplate.from_messages([("system", fallback[0]["content"]), ("user", image_payload)])
            logger.error("Unexpected structure for fallback prompt.")
            raise ValueError("Unexpected structure for fallback prompt.")
        langchain_prompt = langfuse_prompt.get_langchain_prompt()

        langchain_prompt[-1] = ("user", json.loads(langchain_prompt[-1][1]))

        return ChatPromptTemplate.from_messages(langchain_prompt)
