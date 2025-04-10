import io
import pytest
from PIL import Image
import inject
from inject import Binder
from langchain_core.language_models.fake_chat_models import FakeListChatModel

from langchain_ocr_lib.impl.converter.image_converter import Image2MarkdownConverter
from langchain_ocr_lib.di_binding_keys.binding_keys import LargeLanguageModelKey
from langchain_ocr_lib.di_config import lib_di_config


def configure4testing(binder: Binder):
    # This function is used to configure the test environment.
    # It can be used to set up any necessary configurations or dependencies.
    binder.install(lib_di_config)
    binder.bind(LargeLanguageModelKey, FakeListChatModel(responses=["dummy markdown"]))


inject.configure(configure4testing, allow_override=True, clear=True)

# Create a small dummy image and get its PNG bytes to compare later.
dummy_image = Image.new("RGB", (10, 10), color="red")
buf = io.BytesIO()
dummy_image.save(buf, format="PNG")
dummy_image_bytes = buf.getvalue()


@pytest.mark.asyncio
async def test_aconvert2markdown_with_file():
    # Prepare the converter with a dummy chain that asserts on the image data.
    converter = Image2MarkdownConverter()

    # Call aconvert2markdown with a PIL image instance.
    result = await converter.aconvert2markdown(file=dummy_image)
    assert result == "dummy markdown"


@pytest.mark.asyncio
async def test_aconvert2markdown_with_filename(tmp_path):
    # Write the dummy image to a temporary file.
    image_path = tmp_path / "dummy.png"
    dummy_image.save(image_path, format="PNG")

    converter = Image2MarkdownConverter()

    result = await converter.aconvert2markdown(filename=str(image_path))
    assert result == "dummy markdown"


def test_convert2markdown_with_file():
    # Prepare the converter with a dummy chain that asserts on the image data.
    converter = Image2MarkdownConverter()

    # Call convert2markdown with a PIL image instance.
    result = converter.convert2markdown(file=dummy_image)
    assert result == "dummy markdown"


def test_convert2markdown_with_filename(tmp_path):
    # Write the dummy image to a temporary file.
    image_path = tmp_path / "dummy.png"
    dummy_image.save(image_path, format="PNG")

    converter = Image2MarkdownConverter()

    result = converter.convert2markdown(filename=str(image_path))
    assert result == "dummy markdown"


@pytest.mark.asyncio
async def test_aconvert2markdown_no_input():
    # Test that ValueError is raised if neither file nor filename is provided.
    converter = Image2MarkdownConverter()
    with pytest.raises(ValueError):
        await converter.aconvert2markdown()


@pytest.mark.asyncio
async def test_aconvert2markdown_with_corrupted_filename(tmp_path):
    # Create a temporary file with invalid image content.
    corrupt_path = tmp_path / "corrupt.txt"
    corrupt_path.write_text("this is not an image")

    converter = Image2MarkdownConverter()
    with pytest.raises(ValueError, match="Image corrupted or unsupported file type"):
        await converter.aconvert2markdown(filename=str(corrupt_path))


def test_convert2markdown_no_input():
    # Test that ValueError is raised if neither file nor filename is provided.
    converter = Image2MarkdownConverter()
    with pytest.raises(ValueError):
        converter.convert2markdown()


def test_convert2markdown_with_corrupted_filename(tmp_path):
    # Create a temporary file with invalid image content.
    corrupt_path = tmp_path / "corrupt.txt"
    corrupt_path.write_text("this is not an image")

    converter = Image2MarkdownConverter()
    with pytest.raises(ValueError, match="Image corrupted or unsupported file type"):
        converter.convert2markdown(filename=str(corrupt_path))
