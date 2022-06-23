"""
test for module my_utilities.view.pdf_maker
"""
# pylint: disable=too-few-public-methods,too-many-locals,invalid-name,too-many-statements,broad-except,no-value-for-parameter,unexpected-keyword-arg # noqa

import os
from pathlib import Path
from typing import Union

import pandas as pd
import pdfplumber
import pytest
from PIL import Image

from my_utilities.view.pdf_maker import (
    Block,
    BlockImage,
    BlockTable,
    BlockText,
    PDFIncorrectType,
    PDFMaker,
    PDFWrongTypeBlock,
    PDFWrongTypeData,
)


class CustomTextBlock(Block):
    """CustomTextBlock"""

    type_block = "custom_text"
    is_new_page = True
    new_text: str


def function_custom_handler(self: PDFMaker, block: CustomTextBlock):
    """
     example custom handler
    :param self:
    :param block:
    :return:
    """
    if block.is_new_page or not self.is_init_page:
        self.pdf_file.add_page()
        self.is_init_page = True
    self.pdf_file.cell(w=200, h=10, txt=block.new_text)


def remove_file(path_to_file):
    """

    :param path_to_file: path to file which remove
    :return:
    """
    try:
        os.remove(path_to_file)
    except Exception:
        pass


def get_text_from_page(path_to_pdf: Union[str, Path], page: int = 0) -> str:
    """
    :param path_to_pdf: path to file
    :param page: num page
    :return:
    """
    with pdfplumber.open(path_to_pdf) as pdf:
        first_page = pdf.pages[page]
        return first_page.extract_text()


def get_count_pages_pdf(path_to_pdf: Union[str, Path]) -> int:
    """
    :param path_to_pdf: path to file
    :return:
    """
    with pdfplumber.open(path_to_pdf) as pdf:
        return len(pdf.pages)


def get_img(path_to_img: Path):
    """
    generate img for test
    :param path_to_img:
    :return:
    """
    width = 400
    height = 300

    img = Image.new(mode="RGB", size=(width, height), color=(209, 123, 193))
    img.save(path_to_img)


def test_pdf_maker():
    """
    test pdf_maker
    :return:
    """
    path_to_file = Path("./file.pdf")
    remove_file(path_to_file)
    path_to_pdf = Path("./test.pdf")
    remove_file(path_to_pdf)
    path_to_img = Path("./img.png")
    get_img(path_to_img)

    df = pd.DataFrame({"A": [2, 4, 6], "B": [3, 5, 7]})

    num_page = 0
    pdf = PDFMaker(styles=None)
    txtb = BlockText(
        text_to_add="test text",
        is_new_page=True,
        with_line=True,
        ln=3,
        count_ln_after=2,
    )
    multitxtb = BlockText(
        text_to_add="test text",
        is_multi_cell=True,
        is_new_page=True,
        with_line=True,
        ln=3,
        count_ln_after=2,
    )
    tmptxtb = BlockText(text_to_add="test text")
    ctxtb = CustomTextBlock(new_text="test custom text")
    table_block = BlockTable(
        table=df,
        with_index=True,
        is_new_page=True,
        is_specific_last_column=True,
        is_specific_last_row=True,
    )
    tmptable_block = BlockTable(table=df, with_index=True)
    img_block = BlockImage(img=path_to_img, alt_text="alt_text", is_new_page=True)
    tmpimg_block = BlockImage(img=path_to_img)
    incorrect_img_block = BlockImage(
        img="incorrect.png", alt_text="alt_text", is_new_page=True
    )
    with pytest.raises(TypeError):
        pdf.add_block(PDFMaker())
    with pytest.raises(KeyError):
        pdf.add_custom_block_handler("text", function_custom_handler)
    with pytest.raises(PDFIncorrectType):
        pdf.add_img(ctxtb)
    with pytest.raises(PDFIncorrectType):
        pdf.add_table(ctxtb)
    with pytest.raises(PDFIncorrectType):
        pdf.add_text_row(ctxtb)
    with pytest.raises(PDFWrongTypeBlock):
        pdf.add_block(ctxtb)
    with pytest.raises(PDFWrongTypeData):
        incorrect_txtb = BlockText(
            text_to_add=df, is_new_page=True, with_line=True, ln=3
        )
        pdf.add_block(incorrect_txtb)
    with pytest.raises(PDFWrongTypeData):
        incorrect_table = BlockTable(table=123)
        pdf.add_block(incorrect_table)
    with pytest.raises(TypeError):
        pdf.add_custom_block_handler("test", function_custom_handler=1)  # noqa
    with pytest.raises(TypeError):
        pdf = PDFMaker(styles=PDFMaker)  # noqa

    remove_file(path_to_pdf)
    pdf = PDFMaker()
    pdf.add_custom_block_handler(CustomTextBlock.type_block, function_custom_handler)
    pdf.add_block(ctxtb)
    remove_file(path_to_pdf)
    assert path_to_pdf.is_file() is False
    path_to_pdf = pdf.save(file_name=path_to_pdf)
    assert path_to_pdf.is_file() is True
    assert get_text_from_page(path_to_pdf, num_page) == ctxtb.new_text
    pdf = PDFMaker()
    pdf.add_block(txtb)
    path_to_pdf = pdf.save(file_name=path_to_pdf)
    assert get_text_from_page(path_to_pdf, num_page) == txtb.text_to_add
    pdf = PDFMaker()
    pdf.add_block(txtb)
    pdf.add_block(multitxtb)
    pdf.add_block(table_block)
    path_to_pdf = pdf.save(file_name=path_to_pdf)
    pdf = PDFMaker()
    pdf.add_block(txtb)
    pdf.add_block(img_block)
    pdf.add_block(incorrect_img_block)
    path_to_pdf = pdf.save(file_name=path_to_pdf)
    assert get_text_from_page(path_to_pdf, 2) == incorrect_img_block.alt_text

    pdf = PDFMaker()
    pdf.add_block(tmptxtb)
    pdf = PDFMaker()
    pdf.add_block(tmpimg_block)
    pdf = PDFMaker()
    pdf.add_block(tmptable_block)
    pdf = PDFMaker()
    txtb_link_from = BlockText(
        text_to_add="from link",
        with_line=True,
        ln=3,
        link_to="link",
    )
    txtb_link_to = BlockText(
        text_to_add="link to", is_new_page=True, with_line=True, ln=3, add_link="link"
    )
    list_blocks = [
        txtb,
        txtb_link_from,
        incorrect_img_block,
        ctxtb,
        table_block,
        img_block,
        txtb_link_to,
    ]
    with pytest.raises(PDFWrongTypeBlock):
        pdf.add_blocks(list_blocks)
    pdf = PDFMaker()
    pdf.add_custom_block_handler(ctxtb.type_block, function_custom_handler)
    pdf.add_blocks(list_blocks)
    path_to_pdf = pdf.save(path_to_pdf)
    assert get_count_pages_pdf(path_to_pdf) == 6
    pdf = PDFMaker()
    pdf.add_block(txtb_link_to)
    pdf.add_block(txtb_link_from)

    remove_file(path_to_pdf)
    remove_file("./DejaVuSansCondensed.pkl")
    remove_file("./file.pdf")
    remove_file(path_to_img)
