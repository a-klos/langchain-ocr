"""Module containing the dependency injection container for managing application dependencies."""

# Using the inject package for dependency injection configuration

from inject import Binder
import inject
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


def _di_config(binder: Binder):
    langfuse_settings = LangfuseSettings()
    llm_class_type_settings = LlmClassTypeSettings()
    language_settings = LanguageSettings()

    if llm_class_type_settings.llm_type == "ollama":
        settings = OllamaSettings()
        llm_instance = llm_provider(settings, ChatOllama)
    elif llm_class_type_settings.llm_type == "openai":
        settings = OpenAISettings()
        llm_instance = llm_provider(settings, ChatOpenAI)
    else:
        raise NotImplementedError("Configured LLM is not implemented")
    binder.bind("LargeLanguageModel", llm_instance)
    
    prompt = ocr_prompt_template_builder(language=language_settings.language, model_name=settings.model)
    
    langfuse_client = Langfuse(
        public_key=langfuse_settings.public_key,
        secret_key=langfuse_settings.secret_key,
        host=langfuse_settings.host,
    )
    binder.bind("LangfuseClient", langfuse_client)
    
    langfuse_manager = LangfuseManager(
        langfuse=langfuse_client,
        managed_prompts={
            OcrChain.__name__: prompt,
        },
        llm=llm_instance,
    )
    binder.bind("LangfuseManager", langfuse_manager)
    
    ocr_chain = OcrChain(
        langfuse_manager=langfuse_manager,
    )
    binder.bind("OcrChain", ocr_chain)
    
    traced_ocr_chain = LangfuseTracedChain(
        inner_chain=ocr_chain,
        settings=langfuse_settings,
    )
    binder.bind("LangfuseTracedChain", traced_ocr_chain)
    
    binder.bind("ConvertPdfEndpoint", ConvertPdfEndpoint(chain=traced_ocr_chain))
    binder.bind("ConvertImageEndpoint", ConvertImageEndpoint(chain=traced_ocr_chain))
    
def configure_di():
    inject.configure(_di_config, allow_override=True)
