"""Module containing the dependency injection container for managing application dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (  # noqa: WOT001
    Configuration,
    Selector,
    Singleton,
)

from langchain_ollama import ChatOllama
from langchain_community.llms.vllm import VLLMOpenAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langfuse import Langfuse

from langchain_ocr.impl.api_endpoints.convert_image_endpoint import ConvertImageEndpoint
from langchain_ocr.impl.api_endpoints.convert_pdf_endpoint import ConvertPdfEndpoint
from langchain_ocr.impl.chains.ocr_chain import OcrChain
from langchain_ocr.impl.settings.ollama_chat_settings import OllamaSettings
from langchain_ocr.impl.settings.openai_chat_settings import OpenAISettings
from langchain_ocr.impl.settings.llm_class_type_settings import LlmClassTypeSettings
from langchain_ocr.impl.settings.langfuse_settings import LangfuseSettings
from langchain_ocr.impl.settings.language_settings import LanguageSettings
from langchain_ocr.impl.tracers.langfuse_traced_chain import LangfuseTracedChain
from langchain_ocr.prompt_templates.ocr_prompt import ocr_prompt_template_builder
from langchain_ocr.impl.llms.llm_factory import llm_provider
from langchain_ocr.impl.langfuse_manager.langfuse_manager import LangfuseManager



class DependencyContainer(DeclarativeContainer):
    """Dependency injection container for managing application dependencies."""

    class_selector_config = Configuration()

    # Settings
    ollama_settings = OllamaSettings()
    openai_settings = OpenAISettings()
    langfuse_settings = LangfuseSettings()
    llm_class_type_settings = LlmClassTypeSettings()
    language_settings = LanguageSettings()
    class_selector_config.from_dict(llm_class_type_settings.model_dump())

    large_language_model = Selector(
        class_selector_config.llm_type,
        ollama=Singleton(llm_provider, ollama_settings, ChatOllama),
        openai=Singleton(llm_provider, openai_settings, ChatOpenAI),
    )
    
    settings_of_interest = {
        "ollama": ollama_settings,
        "openai": openai_settings,
    }
        
    prompt = ocr_prompt_template_builder(language=language_settings.language, model_name=settings_of_interest[llm_class_type_settings.llm_type].model)

    langfuse = Singleton(
        Langfuse,
        public_key=langfuse_settings.public_key,
        secret_key=langfuse_settings.secret_key,
        host=langfuse_settings.host,
    )

    langfuse_manager = Singleton(
        LangfuseManager,
        langfuse=langfuse,
        managed_prompts={
            OcrChain.__name__: prompt,
        },
        llm=large_language_model,
    )

    ocr_chain = Singleton(
        OcrChain,
        langfuse_manager=langfuse_manager,
    )

    # wrap graph in tracer
    traced_ocr_chain = Singleton(
        LangfuseTracedChain,
        inner_chain=ocr_chain,
        settings=langfuse_settings,
    )
    
    convert_pdf_endpoint = Singleton(
        ConvertPdfEndpoint,
        chain=traced_ocr_chain,
    )
    
    convert_image_endpoint = Singleton(
        ConvertImageEndpoint,
        chain=traced_ocr_chain,
    )

