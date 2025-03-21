from langchain.prompts import ChatPromptTemplate

from langchain_ocr.language_mapping.language_mapping import get_language_name_from_pycountry

def ocr_prompt_template_builder(language:str="en", model_name:str="") -> str:
    system_prompt = f"""
    You are an advanced OCR tool. Your task is to extract all text content from this image in {get_language_name_from_pycountry(language)} **verbatim**, without any modifications, interpretations, summarizations, or omissions. **It is imperative that you do not add, infer, or hallucinate any content that is not explicitly present in the image.**

    **Requirements:** , adhering to the following guidelines:

    - **Headers:** Use Markdown headers (`#`, `##`, `###`, etc.) **only if corresponding heading structures are explicitly present in the image**. Match the level of the header accurately.
    - **Lists:** Preserve all original list formats (unordered lists using `-` or `*`, and ordered lists with numbers) **exactly as they appear** in the image. Maintain indentation.
    - **Text Formatting:** Retain all visual text formatting (bold, italics, underlines, strikethrough, etc.) using the appropriate Markdown syntax (`**bold**`, `*italic*`, `<u>underline</u>`, `~~strikethrough~~`). If a direct Markdown equivalent doesn't exist, prioritize accuracy of the text content.
    - **Code Blocks:** If code or preformatted text is detected (often with a distinct font or background), format it using Markdown code blocks (using backticks ```).
    - **Tables:** If tabular data is present, attempt to format it as a Markdown table using pipes `|` and hyphens `-`. If the table structure is complex, prioritize accurate text extraction over perfect table formatting.
    - **Spacing and Line Breaks:** Maintain original line breaks and spacing to preserve the original layout as much as possible.
    
    **Requirmenets:**
    - **Text Extraction:** Extract all text content from the image, including headings, paragraphs, lists, tables, and any other textual elements.
    - **Complete Content:** Do **not omit** any part of the page, including headers, footers, and subtext.
    - **Replicate formatting:** Preserve the original formatting, including bold, italics, underlines, and other visual styles.
    """
    
    if "llama3.2" in model_name:
        system_prompt = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>"+system_prompt+"<|eot_id|>"


    
    ocr_prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", [
            {
                "type": "image_url",
                "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
            }
        ])
    ])

    return ocr_prompt_template