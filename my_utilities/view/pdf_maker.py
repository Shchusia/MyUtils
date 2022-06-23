"""
Module for build pdf files
"""
# pylint: disable=duplicate-code,too-few-public-methods,bad-option-value,broad-except,use-maxsplit-arg, use-dict-literal,use-list-literal, too-many-instance-attributes,bare-except # noqa

from __future__ import annotations

import os
from dataclasses import dataclass
from logging import Logger
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import pandas as pd
from fpdf import FPDF

SYMBOLS_TO_EXCLUDE = [
    "є",
]

DEFAULT_LOGGER = Logger(__name__)

BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__))).parent
PATH_TO_SRC_FOLDER = BASE_DIR / "src"
DEFAULT_TTF_FILE = "DejaVuSansCondensed.ttf"
DEFAULT_FONT = "DejaVu"


class PDFMakerException(Exception):
    """
    class exception builder
    """


class PDFWrongTypeData(PDFMakerException):
    """
    wrong type
    """

    def __init__(self, msg: str = ""):
        if msg:
            self.message = f"`data` must be a {msg}"
        else:
            self.message = "Wrong `data` type."
        super().__init__(self.message)


class PDFWrongTypeBlock(PDFMakerException):
    """
    wrong type
    """

    def __init__(self, incorrect_type: str):
        self.incorrect_type = incorrect_type
        self.message = (
            f"Not exist function for build block with type {self.incorrect_type}"
        )
        super().__init__(self.message)


class PDFIncorrectType(PDFMakerException):
    """
    exception for incorrect blocks
    """

    def __init__(self, required: str, provided: str):
        self.message = (
            "You passed the wrong block to the function to add."
            f" An `{required}` is required, not `{provided}`"
        )
        super().__init__(self.message)


class Block:
    """
    Base class for all rows
    """

    @property
    def type_block(self) -> str:
        """
        Must override type_block in sub classes for choice function build block
        :return: none
        """
        raise NotImplementedError

    style: str = ""
    size: int = 14
    font: str = None
    align: str = ""
    x: int = None
    y: int = None
    w: int = 0
    h: int = 0
    ln: int = 0
    fill: bool = False
    border: int = 0
    count_ln_after: int = 1
    is_new_page: bool = False
    link: str = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class BlockText(Block):
    """
    class for text block
    """

    type_block = "text"
    text_to_add: str
    text_color: Tuple[int, int, int] = (0, 0, 0)  # rgb
    link_to: Any = None
    add_link: Any = None
    is_multi_cell: bool = False
    max_line_height: int = 2
    split_only: bool = False
    with_line: bool = False


class BlockTable(Block):
    """
    class for table block
    """

    type_block = "table"

    table: pd.DataFrame
    with_index: bool = False
    is_specific_last_row: bool = False
    is_specific_last_column: bool = False

    table_header_background_color: Tuple[int, int, int] = (47, 79, 79)
    specific_last_row_color: Tuple[int, int, int] = (169, 255, 51)
    specific_last_column_color: Tuple[int, int, int] = (169, 255, 51)

    colors_rows: List[Tuple[int, int, int]] = [
        (237, 238, 224),
        (221, 223, 198),
    ]


class BlockImage(Block):
    """
    class for img block
    """

    type_block = "img"
    img: Union[Path, str]
    alt_text: str = ""


@dataclass
class DefaultStylesPDF:
    """
    class with default styles
    """

    default_orientation: Optional[str] = "P"
    default_page_unit: Optional[str] = "mm"
    default_page_format: Optional[str] = "A4"
    is_font_uni: Optional[bool] = True

    # font conf
    default_font_size: Optional[int] = 14
    default_font_style: Optional[str] = ""
    default_ln: Optional[int] = 5


class PDFMaker:
    """
    class for build pdf files
    """

    pdf_file = None
    links: Dict[Any, Any]
    is_saved = False
    is_init_page = False

    types_function = {
        "text": "add_text_row",
        "table": "add_table",
        "img": "add_img",
    }  # type: Dict[str, str]
    tf_to_execute: Dict[str, Callable]
    custom_functions: List[str]

    def __init__(
        self,
        path_to_ttf_file: Optional[Union[Path, str]] = None,
        font: str = "",
        styles: DefaultStylesPDF = None,
        logger: Optional[Logger] = None,
    ):
        self._logger = logger or DEFAULT_LOGGER
        if not styles:
            styles = DefaultStylesPDF()
            self._logger.info("%s use default styles", self.__class__.__name__)
        if not isinstance(styles, DefaultStylesPDF):
            raise TypeError(f"styles must be a DefaultStylesPDF and not {type(styles)}")
        self.styles = styles
        if not path_to_ttf_file:  # pragma: no cover
            path_to_ttf_file = PATH_TO_SRC_FOLDER / DEFAULT_TTF_FILE
            font = DEFAULT_FONT
        if not font:  # pragma: no cover
            font = DEFAULT_FONT

        self.pdf_font = font
        self.path_to_ttf_file = path_to_ttf_file
        self.pdf_file = FPDF(
            orientation=styles.default_orientation,
            unit=styles.default_page_unit,
            format=styles.default_page_format,
        )
        self.pdf_file.add_font(
            family=self.pdf_font,
            style=self.styles.default_font_style,
            fname=self.path_to_ttf_file,
            uni=self.styles.is_font_uni,
        )
        self.pdf_file.set_font(
            family=self.pdf_font,
            style=self.styles.default_font_style,
            size=self.styles.default_font_size,
        )
        self.links = dict()
        self.tf_to_execute = dict()
        self.custom_functions = list()
        self._init_existed_functions()

    def __del__(self):
        if not self.is_saved:
            try:
                self.save()
            except:  # pragma: no cover # noqa
                pass

    def _init_existed_functions(self) -> None:
        """
        Function for validate inputted functions
        and init tf_to_execute types_function_to_execute
        :return: nothing
        """
        for type_block, function_to_add in self.types_function.items():
            function = getattr(self, function_to_add)
            if function and callable(function):  # pragma: no cover
                self.tf_to_execute[type_block] = function
                continue
            raise ValueError(  # pragma: no cover
                f"Class {self.__class__.__name__} don't have a function"
                f" - {function_to_add} or it's not a function. Type - {type_block} "
            )

    def save(self, file_name: Optional[Union[str, Path]] = None) -> Optional[Path]:
        """
        function for save pdf
        :param Optional[str] file_name:  name_file
        :return: path to saved file
        """
        try:
            self.is_saved = True
            if not file_name:
                file_name = "file"

            if str(file_name).split(".")[-1] != "pdf":
                file_name = str(file_name) + ".pdf"
            self.pdf_file.output(name=file_name, dest="f")
            return Path(file_name)
        except Exception as exc:
            self._logger.error("File not saved. Reason: %s", str(exc), exc_info=True)
        return None

    def add_block(self, block: Block):
        """

        :param block:
        :return:
        """
        self.is_saved = False
        if not isinstance(block, Block):
            raise TypeError(f"block must be Block and not {type(block)}")
        function_to_execute = self.tf_to_execute.get(block.type_block, None)
        if function_to_execute and callable(function_to_execute):
            if function_to_execute.__name__ in self.custom_functions:
                function_to_execute(self, block)
            else:
                function_to_execute(block)
            return
        raise PDFWrongTypeBlock(block.type_block)

    def add_blocks(self, blocks: List[Block]):
        """

        :param blocks:
        :return:
        """
        for block in blocks:
            self.add_block(block)

    def add_text_row(self, block: BlockText) -> None:
        """
        function add text
        :param block:
        :return:
        """
        # if not isinstance(block, BlockText):
        #     raise PDFIncorrectType(required=BlockText.type_block,
        #                            provided=getattr(block, "type_block", 'unknown'))
        self.validate_block(BlockText, block)

        if not isinstance(block.text_to_add, str):
            raise PDFWrongTypeData("str")
        if block.is_new_page or not self.is_init_page:
            self.pdf_file.add_page()
            self.is_init_page = True

        self.pdf_file.set_text_color(*block.text_color)

        link = block.link

        if block.link_to:
            _link = self.pdf_file.add_link()
            self.pdf_file.set_link(_link)
            self.links[block.link_to] = _link
            link = _link

        if block.add_link:
            if self.links.get(block.add_link):
                self.pdf_file.set_link(self.links[block.add_link])
            else:
                self._logger.warning("not found link: `%s`", block.add_link)

        self.pdf_file.set_font(
            block.font or self.pdf_font, style=block.style, size=block.size
        )
        if block.is_multi_cell:
            self.pdf_file.multi_cell(
                block.w,
                block.h,
                txt=block.text_to_add,
                border=block.border,
                align=block.align,
                fill=block.fill,
                split_only=block.split_only,
            )
        else:
            self.pdf_file.cell(
                w=block.w,
                h=block.h,
                txt=block.text_to_add,
                border=block.border,
                ln=block.ln,
                align=block.align,
                fill=block.fill,
                link=link,
            )
        if block.with_line:
            self.pdf_file.line(
                10,
                self.pdf_file.get_y() + 5 * (block.count_ln_after - 1),
                200,
                self.pdf_file.get_y() + 5 * (block.count_ln_after - 1),
            )
        self._add_rows(block.count_ln_after)

    def add_table(self, block: BlockTable) -> None:
        """
        add table to pdf
        :param BlockTable block:
        :return: nothing
        """

        def make_table_header(columns):
            self.pdf_file.set_fill_color(*block.table_header_background_color)
            for item in columns:
                self.pdf_file.cell(
                    col_width,
                    row_height * spacing,
                    txt=str(item),
                    border=block.border,
                    fill=True,
                )
            self.pdf_file.ln(row_height * spacing)

        def make_row_table(columns):
            for k, item in enumerate(columns):
                if block.is_specific_last_column and (k + 1) == len(columns):
                    self.pdf_file.set_fill_color(*block.specific_last_column_color)
                self.pdf_file.cell(
                    col_width,
                    (row_height * spacing),
                    txt=str(item),
                    border=block.border,
                    fill=True,
                )
            self.pdf_file.ln(row_height * spacing)

        # if not isinstance(block, BlockTable):
        #     raise PDFIncorrectType(required=BlockTable.type_block,
        #                            provided=getattr(block, "type_block", 'unknown'))
        self.validate_block(BlockTable, block)

        if block.is_new_page or not self.is_init_page:  # pragma: no cover
            self.pdf_file.add_page()
            self.is_init_page = True

        self.pdf_file.set_font(
            block.font or self.pdf_font, style=block.style, size=block.size
        )

        spacing = 1
        col_width = self.pdf_file.w / 4.5
        row_height = self.pdf_file.font_size
        if not isinstance(block.table, pd.DataFrame):
            raise PDFWrongTypeData("DataFrame")
        col = list(block.table.columns)
        if block.with_index:  # pragma: no cover
            col.insert(0, "")
        col_width = self.pdf_file.w / len(col) + 0.5
        make_table_header(col)
        for i, val in block.table.iterrows():
            list_val = list(val)
            if block.with_index:  # pragma: no cover
                list_val.insert(0, str(i))
            if block.is_specific_last_row and (i + 1) == len(block.table):
                self.pdf_file.set_fill_color(*block.specific_last_row_color)
            else:
                current_color_id = i % len(block.colors_rows)
                self.pdf_file.set_fill_color(*block.colors_rows[current_color_id])
            make_row_table(list_val)

        self._add_rows(block.count_ln_after)

    @staticmethod
    def validate_block(required_block_type: Type[Block], received_block: Block) -> None:
        """
        Function for validate blocks for methods
        :param Type[Block] required_block_type:
        :param received_block:
        :return: nothing
        :raise PDFIncorrectType: if incorrect block
        """
        if not isinstance(received_block, required_block_type):
            raise PDFIncorrectType(
                required=required_block_type.type_block,  # type: ignore
                provided=getattr(received_block, "type_block", "unknown"),
            )

    def add_img(self, block: BlockImage) -> None:
        """
        add image to file
        :param block:
        :return: nothing
        """
        # if not isinstance(block, BlockImage):
        #     raise PDFIncorrectType(required=BlockImage.type_block,
        #                            provided=getattr(block, "type_block", 'unknown'))
        self.validate_block(BlockImage, block)
        if block.is_new_page or not self.is_init_page:  # pragma: no cover
            self.pdf_file.add_page()
            self.is_init_page = True
        self.pdf_file.set_font(
            block.font or self.pdf_font, style=block.style, size=block.size
        )
        try:
            self.pdf_file.image(
                name=str(block.img),
                x=block.x,
                y=block.y,
                w=block.w,
                h=block.h,
                link=block.link,
            )
        except FileNotFoundError:
            self._logger.warning("file not found: %s", block.img, exc_info=True)
            self.pdf_file.cell(
                w=block.w,
                h=block.h,
                txt=block.alt_text,
                border=block.border,
                ln=block.ln,
                align=block.align,
                fill=block.fill,
            )

        self._add_rows(block.count_ln_after)

    def _add_rows(self, count_rows: int = 1):
        """
        Method to add empty rows after block
        :param count_rows:
        :return:
        """
        for _ in range(count_rows):
            self.pdf_file.ln(self.styles.default_ln)

    def add_custom_block_handler(
        self,
        new_type_block: str,
        function: Callable[[PDFMaker, Block], None],
        is_override: bool = False,
    ):
        """
        Add custom block handler for custom blocks
        :param new_type_block:
        :param function:
        :param is_override:
        :return:
        """
        if not callable(function):  # pragma: no cover
            raise TypeError("function must be callable")
        if self.tf_to_execute.get(new_type_block) and not is_override:
            raise KeyError(
                f"In {self.__class__.__name__} exist function for "
                f"block type {new_type_block}. Change type_block or"
                f" set `is_override` - True to override existed function"
            )
        self.custom_functions.append(function.__name__)
        self.tf_to_execute[new_type_block] = function
