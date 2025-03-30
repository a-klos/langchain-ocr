"""Module containing the dependency injection container for managing application dependencies."""

from inject import Binder
import inject
from langchain_ocr_lib.di_config import lib_di_config

from langchain_ocr.impl.api_endpoints.convert_image_endpoint import ConvertImageEndpoint
from langchain_ocr.impl.api_endpoints.convert_pdf_endpoint import ConvertPdfEndpoint


def _api_specific_config(binder: Binder):
    binder.install(lib_di_config)
    binder.bind("ConvertPdfEndpoint", ConvertPdfEndpoint())
    binder.bind("ConvertImageEndpoint", ConvertImageEndpoint())


def configure():
    """Configure the dependency injection container."""
    inject.configure(_api_specific_config, allow_override=True, clear=False)
