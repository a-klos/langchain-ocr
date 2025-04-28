"""Module to create a Gradio UI for LangChain OCR."""

import gradio as gr
from gradio_pdf import PDF
from pathlib import Path

from gradio_ui.converter import Converter


def _perform_ocr(doc: str) -> str:
    converter = Converter()
    return converter.convert(filename=doc)


def main():
    """Run the Gradio app."""
    with gr.Blocks(
        title="Langchain-OCR Playground",
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="cyan"),
    ) as demo:
        gr.Markdown("# 📄 LangChain-OCR Playground")
        gr.Markdown(
            """
            Upload a PDF file and extract structured text using LLM-powered OCR.

            The application will convert your document to markdown format.
            """
        )
        dir_ = Path(__file__).parent
        gr.Interface(
            _perform_ocr,
            [PDF(label="PDF Document")],
            gr.Markdown(
                label="Output (Markdown)",
                min_height=270,
                container=True,
                show_copy_button=True,
            ),
            examples=[
                [str(dir_ / "examples" / "invoice.pdf")],
                [str(dir_ / "examples" / "invoice-hw.pdf")],
            ],
        )
    demo.launch()


if __name__ == "__main__":
    main()
