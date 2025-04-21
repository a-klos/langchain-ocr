import gradio as gr
from gradio_pdf import PDF
from pathlib import Path

from gradio_ui.converter import Converter


def perform_ocr(doc: str) -> str:
    converter = Converter()
    return converter.convert(filename=doc)


def build_ui() -> gr.Blocks:
    with gr.Blocks(
        title="Langchain-OCR",
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="cyan"),
    ) as demo:
        gr.Markdown("# LangChain-OCR show case")
        gr.Markdown(
            """
            Upload a PDF or image file. The application will:
            1. perform OCR powered by TogetherAI`s Llama Vision 11B
            2. output structured text in markdown format
            """
        )
        dir_ = Path(__file__).parent
        gr.Interface(
            perform_ocr,
            [PDF(label="Document")],
            gr.Textbox(lines=8, label="Markdown output"),
            examples=[
                [str(dir_ / "examples" / "invoice.pdf")],
                [str(dir_ / "examples" / "invoice-hw.pdf")],
            ],
        )

        return demo


def main():
    demo = build_ui()
    import sys

    setattr(sys.modules[__name__], "demo", demo)
    demo.launch()


if __name__ == "__main__":
    main()
