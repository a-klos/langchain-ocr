"""Module containing the dependency injection container for managing application dependencies."""

from inject import Binder
import inject
from langchain_ocr_lib.di_binding_keys.binding_keys import (
    ImageConverterKey,
    LangfuseClientKey,
    LangfuseManagerKey,
    LangfuseTracedChainKey,
    LargeLanguageModelKey,
    OcrChainKey,
    PdfConverterKey,
)
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langfuse import Langfuse
from functools import partial

from langchain_ocr_lib.impl.chains.ocr_chain import OcrChain
from langchain_ocr_lib.impl.settings.ollama_chat_settings import OllamaSettings
from langchain_ocr_lib.impl.settings.vllm_chat_settings import VllmSettings
from langchain_ocr_lib.impl.settings.openai_chat_settings import OpenAISettings
from langchain_ocr_lib.impl.settings.llm_class_type_settings import LlmClassTypeSettings
from langchain_ocr_lib.impl.settings.langfuse_settings import LangfuseSettings
from langchain_ocr_lib.impl.settings.language_settings import LanguageSettings
from langchain_ocr_lib.impl.tracers.langfuse_traced_chain import LangfuseTracedChain
from langchain_ocr_lib.prompt_templates.ocr_prompt import ocr_prompt_template_builder
from langchain_ocr_lib.impl.llms.llm_factory import llm_provider
from langchain_ocr_lib.impl.langfuse_manager.langfuse_manager import LangfuseManager
from langchain_ocr_lib.impl.converter.pdf_converter import Pdf2MarkdownConverter
from langchain_ocr_lib.impl.converter.image_converter import Image2MarkdownConverter


def lib_di_config(binder: Binder):
    """Configure dependency injection bindings for the OCR library.

    Parameters
    ----------
    binder : Binder
        The dependency injection binder instance used to register the bindings.

    Raises
    ------
    NotImplementedError
        If the configured LLM type is not implemented.

    """
    langfuse_settings = LangfuseSettings()
    llm_class_type_settings = LlmClassTypeSettings()
    language_settings = LanguageSettings()

    if llm_class_type_settings.llm_type == "ollama":
        settings = OllamaSettings()
        partial_llm_provider = partial(llm_provider,settings, ChatOllama)
    elif llm_class_type_settings.llm_type == "openai":
        settings = OpenAISettings()
        partial_llm_provider = partial(llm_provider,settings, ChatOpenAI)
    elif llm_class_type_settings.llm_type == "vllm":
        settings = VllmSettings()
        partial_llm_provider = partial(llm_provider,settings, ChatOpenAI)
    else:
        raise NotImplementedError("Configured LLM is not implemented")
    
    binder.bind_to_provider(LargeLanguageModelKey, partial_llm_provider)

    prompt = ocr_prompt_template_builder(language=language_settings.language, model_name=settings.model)

    binder.bind(
        LangfuseClientKey,
        Langfuse(
            public_key=langfuse_settings.public_key,
            secret_key=langfuse_settings.secret_key,
            host=langfuse_settings.host,
        ),
    )

    binder.bind(
        LangfuseManagerKey,
        LangfuseManager(
            managed_prompts={
                OcrChain.__name__: prompt,
            },
            enabled=langfuse_settings.enabled,
        ),
    )

    binder.bind(OcrChainKey if langfuse_settings.enabled else LangfuseTracedChainKey, OcrChain())

    if langfuse_settings.enabled:
        binder.bind(
            LangfuseTracedChainKey,
            LangfuseTracedChain(
                settings=langfuse_settings,
            ),
        )

    binder.bind(PdfConverterKey, Pdf2MarkdownConverter())
    binder.bind(ImageConverterKey, Image2MarkdownConverter())


def configure_di():
    """Configure dependency injection using the `inject` library."""
    inject.configure(lib_di_config, allow_override=True, clear=True)
