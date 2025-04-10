import io
import pytest
import inject
from inject import Binder
from langchain_ocr_lib.di_binding_keys.binding_keys import LargeLanguageModelKey
from langchain_ocr_lib.di_config import lib_di_config
from langchain_ocr_lib.impl.converter.pdf_converter import Pdf2MarkdownConverter
from langchain_core.language_models.fake_chat_models import FakeListChatModel

# A minimal dummy PDF content.
dummy_pdf_bytes = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT
/F1 24 Tf
100 100 Td
(dummy pdf) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000010 00000 n 
0000000060 00000 n 
0000000110 00000 n 
0000000170 00000 n 
trailer
<< /Root 1 0 R /Size 5 >>
startxref
250
%%EOF
"""

def configure4testing(binder: Binder):
    binder.install(lib_di_config)
    binder.bind(LargeLanguageModelKey, FakeListChatModel(responses=["dummy markdown"]))

inject.configure(configure4testing, allow_override=True, clear=True)

@pytest.mark.asyncio
async def test_aconvert2markdown_with_file():
    converter = Pdf2MarkdownConverter()
    result = await converter.aconvert2markdown(file=dummy_pdf_bytes)
    assert result == "dummy markdown"

@pytest.mark.asyncio
async def test_aconvert2markdown_with_filename(tmp_path):
    pdf_path = tmp_path / "dummy.pdf"
    pdf_path.write_bytes(dummy_pdf_bytes)

    converter = Pdf2MarkdownConverter()
    result = await converter.aconvert2markdown(filename=str(pdf_path))
    assert result == "dummy markdown"

def test_convert2markdown_with_file():
    converter = Pdf2MarkdownConverter()
    result = converter.convert2markdown(file=dummy_pdf_bytes)
    assert result == "dummy markdown"

def test_convert2markdown_with_filename(tmp_path):
    pdf_path = tmp_path / "dummy.pdf"
    pdf_path.write_bytes(dummy_pdf_bytes)

    converter = Pdf2MarkdownConverter()
    result = converter.convert2markdown(filename=str(pdf_path))
    assert result == "dummy markdown"

@pytest.mark.asyncio
async def test_aconvert2markdown_no_input():
    converter = Pdf2MarkdownConverter()
    with pytest.raises(ValueError):
        await converter.aconvert2markdown()

def test_convert2markdown_no_input():
    converter = Pdf2MarkdownConverter()
    with pytest.raises(ValueError):
        converter.convert2markdown()

@pytest.mark.asyncio
async def test_aconvert2markdown_with_corrupted_filename(tmp_path):
    corrupt_path = tmp_path / "corrupt.pdf"
    corrupt_path.write_bytes(b"this is not a valid PDF")
    converter = Pdf2MarkdownConverter()
    with pytest.raises(ValueError, match="PDF corrupted or unsupported file type"):
        await converter.aconvert2markdown(filename=str(corrupt_path))

def test_convert2markdown_with_corrupted_filename(tmp_path):
    corrupt_path = tmp_path / "corrupt.pdf"
    corrupt_path.write_bytes(b"this is not a valid PDF")
    converter = Pdf2MarkdownConverter()
    with pytest.raises(ValueError, match="PDF corrupted or unsupported file type"):
        converter.convert2markdown(filename=str(corrupt_path))