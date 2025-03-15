# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from langchain_ocr.apis.ocr_api_base import BaseOcrApi
import langchain_ocr.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)
from fastapi import APIRouter, Path, Request, Response, UploadFile  # noqa: F401

from langchain_ocr.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictBytes, StrictStr
from typing import Any, Tuple, Union
from typing_extensions import Annotated
from langchain_ocr.models.convert_pdf_post400_response import ConvertPdfPost400Response


router = APIRouter()

ns_pkg = langchain_ocr.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/convert/docx",
    responses={
        200: {"model": str, "description": "Markdown conversion successful"},
        400: {"model": ConvertPdfPost400Response, "description": "Invalid input or conversion error"},
        500: {"description": "Internal server error"},
    },
    tags=["default"],
    summary="Convert DOCX to Markdown",
    response_model_by_alias=True,
)
async def convert_docx_post(
    file: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The DOCX file to convert.")] = Form(None, description="The DOCX file to convert."),
) -> str:
    """Accepts a DOCX file and returns its content as Markdown."""
    if not BaseOcrApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseOcrApi.subclasses[0]().convert_docx_post(file)


@router.post(
    "/convert/html",
    responses={
        200: {"model": str, "description": "Markdown conversion successful"},
        400: {"model": ConvertPdfPost400Response, "description": "Invalid input or conversion error"},
        500: {"description": "Internal server error"},
    },
    tags=["default"],
    summary="Convert HTML to Markdown",
    response_model_by_alias=True,
)
async def convert_html_post(
    file: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The HTML file to convert.")] = Form(None, description="The HTML file to convert."),
) -> str:
    """Accepts an HTML file and returns its content as Markdown."""
    if not BaseOcrApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseOcrApi.subclasses[0]().convert_html_post(file)


@router.post(
    "/convert/pdf",
    responses={
        200: {"model": str, "description": "Markdown conversion successful"},
        400: {"model": ConvertPdfPost400Response, "description": "Invalid input or conversion error"},
        500: {"description": "Internal server error"},
    },
    tags=["default"],
    summary="Convert PDF to Markdown",
    response_model_by_alias=True,
)
async def convert_pdf_post(
    body: UploadFile,
    request: Request,
) -> str:
    """Accepts a PDF file and returns its content as Markdown."""
    if not BaseOcrApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseOcrApi.subclasses[0]().convert_pdf_post(file)


@router.post(
    "/convert/pptx",
    responses={
        200: {"model": str, "description": "Markdown conversion successful"},
        400: {"model": ConvertPdfPost400Response, "description": "Invalid input or conversion error"},
        500: {"description": "Internal server error"},
    },
    tags=["default"],
    summary="Convert PPTX to Markdown",
    response_model_by_alias=True,
)
async def convert_pptx_post(
    file: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The PPTX file to convert.")] = Form(None, description="The PPTX file to convert."),
) -> str:
    """Accepts a PPTX file and returns its content as Markdown."""
    if not BaseOcrApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseOcrApi.subclasses[0]().convert_pptx_post(file)
