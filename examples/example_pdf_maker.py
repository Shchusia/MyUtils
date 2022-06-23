"""
example
"""
# pylint: disable=invalid-name,duplicate-code

import os
from pathlib import Path

import pandas as pd
from PIL import Image

from my_utilities.view.pdf_maker import BlockImage, BlockTable, BlockText, PDFMaker


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


def main():
    """
    example build pdf file
    :return:
    """
    title = BlockText(
        text_to_add="Report",
        w=200,
        size=72,
        align="L",
        count_ln_after=3,
    )
    content_part = BlockText(
        text_to_add="PartTopic ⇒",
        w=200,
        size=30,
        align="L",
        count_ln_after=3,
        link_to="topic",
    )
    report_part = BlockText(
        text_to_add="PartTopic",
        w=200,
        size=30,
        align="L",
        count_ln_after=3,
        add_link="topic",
        is_new_page=True,
    )
    description = BlockText(
        text_to_add="Long description Long description "
        "Long description Long description Long description ",
        w=200,
        h=15,
        size=16,
        align="L",
        count_ln_after=3,
        is_multi_cell=True,
    )
    df = pd.DataFrame(
        {
            "A": list(range(5)),
            "B": list(range(5)),
            "C": list(range(5)),
        }
    )

    table = BlockTable(
        table=df,
        with_index=True,
        is_specific_last_column=True,
        is_specific_last_row=True,
    )
    path_to_img = Path("tmp_img.png")
    get_img(path_to_img)
    img_block = BlockImage(img=path_to_img, alt_text="alt_text")
    incorrect_img_block = BlockImage(img="./invalid.png", alt_text="alt_text")
    list_blocks = [
        title,
        content_part,
        report_part,
        description,
        table,
        img_block,
        incorrect_img_block,
    ]
    pdf = PDFMaker()
    pdf.add_blocks(list_blocks)
    os.remove(path_to_img)
    pdf.save("./example.pdf")


if __name__ == "__main__":
    main()
