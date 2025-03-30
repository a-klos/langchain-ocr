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

from langchain_ocr.models.convert_image_post400_response import ConvertImagePost400Response
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
    "/convert/image",
    responses={
        200: {"model": str, "description": "Markdown conversion successful"},
        400: {"model": ConvertImagePost400Response, "description": "Invalid input or conversion error"},
        500: {"description": "Internal server error"},
    },
    tags=["default"],
    summary="Convert Image to Markdown",
    response_model_by_alias=True,
)
async def convert_image_post(
    body: UploadFile,
    request: Request,
) -> str:
    """Accepts an image file (JPEG and PNG) and returns its content as Markdown."""
    if not BaseOcrApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseOcrApi.subclasses[0]().convert_image_post(body, request)


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
    return await BaseOcrApi.subclasses[0]().convert_pdf_post(body, request)
