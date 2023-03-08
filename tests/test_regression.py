import sys

from path import Path

sys.path.insert(0, ".")


from pdf_white_cut.cutter import batch_edit_pdf, edit_pdf
from pdf_white_cut.logger import logger
from pdf_white_cut.parser import get_parser

logger.remove()
logger.add(sys.stderr, level="DEBUG")


class Case:
    input: str
    ignore: int

    def __init__(self, input: str, ignore: int = 0) -> None:
        self.input = input
        self.ignore = ignore

    @property
    def input_path(self):
        return Path("./{}".format(self.input))

    @property
    def output_path(self):
        return Path("./output/{}".format(self.input))


def test_regression() -> None:
    cases = [
        Case("cases/bugfix/error_if_cut_again.pdf"),
        Case("cases/bugfix/no_literal.pdf"),
        Case("cases/bugfix/only_left_bottom.pdf", 0),
    ]
    for case in cases:
        edit_pdf(case.input_path, case.output_path, case.ignore)


def test_bugfix_cut_again() -> None:
    cases = [
        Case("cases/bugfix/error_if_cut_again.pdf"),
        Case("output/cases/bugfix/error_if_cut_again.pdf"),
        Case("cases/bugfix/no_literal.pdf"),
        Case("output/cases/bugfix/no_literal.pdf"),
    ]
    for case in cases:
        edit_pdf(case.input_path, case.output_path, case.ignore)