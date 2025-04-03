#!/usr/bin/env python
"""Command-line interface for langchain-ocr-lib package."""

import argparse
import asyncio
import os
import sys
from typing import Optional

from langchain_ocr_lib.di_config import configure_di
import inject
from langchain_ocr_lib.impl.converter.image_converter import Image2MarkdownConverter
from langchain_ocr_lib.impl.converter.pdf_converter import Pdf2MarkdownConverter


def setup() -> None:
    """Initialize the dependency injection configuration."""
    configure_di()


async def convert_image_file(file_path: str, output_file: Optional[str] = None) -> str:
    """Convert an image file to markdown text.

    Parameters
    ----------
    file_path : str
        Path to the image file
    output_file : Optional[str]
        Path to save the markdown output, if None prints to stdout

    Returns
    -------
    str
        The markdown text
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found", file=sys.stderr)
        sys.exit(1)

    converter = inject.instance(Image2MarkdownConverter)

    # Pass the filename directly to the converter
    result = await converter.aconvert2markdown(file=None, filename=file_path)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Markdown saved to {output_file}")
    else:
        print(result)

    return result


async def convert_pdf_file(file_path: str, output_file: Optional[str] = None) -> str:
    """Convert a PDF file to markdown text.

    Parameters
    ----------
    file_path : str
        Path to the PDF file
    output_file : Optional[str]
        Path to save the markdown output, if None prints to stdout

    Returns
    -------
    str
        The markdown text
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found", file=sys.stderr)
        sys.exit(1)

    converter = inject.instance(Pdf2MarkdownConverter)

    # Pass the filename directly to the converter
    result = await converter.aconvert2markdown(file=None, filename=file_path)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Markdown saved to {output_file}")
    else:
        print(result)

    return result


def main():
    """Run the CLI application."""
    parser = argparse.ArgumentParser(description="Convert images or PDFs to Markdown")
    parser.add_argument("file", help="Path to the image or PDF file")
    parser.add_argument("-o", "--output", help="Output file path (default: print to stdout)", default=None)
    parser.add_argument(
        "-t", "--type", choices=["auto", "image", "pdf"], default="auto", help="File type (default: auto-detect)"
    )

    args = parser.parse_args()

    # Setup dependency injection
    setup()

    file_type = args.type
    if file_type == "auto":
        if args.file.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
            file_type = "image"
        elif args.file.lower().endswith(".pdf"):
            file_type = "pdf"
        else:
            print(f"Error: Could not detect file type of {args.file}", file=sys.stderr)
            sys.exit(1)

    if file_type == "image":
        asyncio.run(convert_image_file(args.file, args.output))
    elif file_type == "pdf":
        asyncio.run(convert_pdf_file(args.file, args.output))


if __name__ == "__main__":
    main()

# langchain-ocr image.png -o output.md
