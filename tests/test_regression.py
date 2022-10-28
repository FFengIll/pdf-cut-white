import sys

sys.path.insert(0, ".")

from path import Path

from pdf_white_cut.logger import logger

from pdf_white_cut.cutter import cut_pdf, batch_cut_pdf
from pdf_white_cut.parser import get_parser


class Case:
    input: str
    ignore: int

    def __init__(self, input: str,ignore:int=0) -> None:
        self.input = input
        self.ignore = ignore

    @property
    def input_path(self):
        return Path("./cases/{}".format(self.input))

    @property
    def output_path(self):
        return Path("./output/{}".format(self.input))


def test_regression() -> None:
    cases = [
        Case("bugfix/error_if_cut_again.pdf"),
        Case("bugfix/no_literal.pdf"),
        Case("bugfix/only_left_bottom.pdf", 0),
    ]
    for case in cases:
        cut_pdf(case.input_path, case.output_path, case.ignore)
