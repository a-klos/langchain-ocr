from langchain_ocr.language_mapping.language_mapping import get_language_name_from_pycountry

def ocr_prompt_template_builder(language:str="en") -> str:
    return f"""
    **For OCR:** Extract all text content from this image in {get_language_name_from_pycountry(language)} **verbatim**, without any modifications, interpretations, summarizations, or omissions.

    **Output Format:** Render the extracted text in Markdown, adhering to the following guidelines:

    - **Headers:** Use Markdown headers (`#`, `##`, `###`, etc.) **only if corresponding heading structures are explicitly present in the image**. Match the level of the header accurately.
    - **Lists:** Preserve all original list formats (unordered lists using `-` or `*`, and ordered lists with numbers) **exactly as they appear** in the image. Maintain indentation.
    - **Text Formatting:** Retain all visual text formatting (bold, italics, underlines, strikethrough, etc.) using the appropriate Markdown syntax (`**bold**`, `*italic*`, `<u>underline</u>`, `~~strikethrough~~`). If a direct Markdown equivalent doesn't exist, prioritize accuracy of the text content.
    - **Code Blocks:** If code or preformatted text is detected (often with a distinct font or background), format it using Markdown code blocks (using backticks ```).
    - **Tables:** If tabular data is present, attempt to format it as a Markdown table using pipes `|` and hyphens `-`. If the table structure is complex, prioritize accurate text extraction over perfect table formatting.
    - **Spacing and Line Breaks:** Maintain original line breaks
    """