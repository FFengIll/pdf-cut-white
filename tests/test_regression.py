import hashlib
import sys

from path import Path

sys.path.insert(0, ".")

from pdf_white_cut.logger import logger
from pdf_white_cut.worker import cut_pdf

logger.remove()
logger.add(sys.stderr, level="DEBUG")


class Case:
    input: str
    ignore: int

    def __init__(self, input: str, ignore: int = 0) -> None:
        self.input = input
        self.ignore = ignore

    @property
    def input_path(self) -> Path:
        return Path("./{}".format(self.input))

    @property
    def output_path(self) -> Path:
        output = Path("./output/{}".format(self.input))
        output.dirname().makedirs_p()
        return output

    @property
    def wanted_path(self) -> Path:
        d, base = self.input_path.dirname(), self.input_path.basename()
        wanted = d / "wanted" / base
        return wanted


def test_regression() -> None:
    cases = [
        Case("cases/bugfix/error_if_cut_again.pdf"),
        Case("cases/bugfix/no_literal.pdf"),
        Case("cases/bugfix/only_left_bottom.pdf", 0),
    ]
    for case in cases:
        cut_pdf(case.input_path, case.output_path, case.ignore)


def test_bugfix_cut_again() -> None:
    cases = [
        Case("cases/bugfix/error_if_cut_again.pdf"),
        Case("output/cases/bugfix/error_if_cut_again.pdf"),
        Case("cases/bugfix/no_literal.pdf"),
        Case("output/cases/bugfix/no_literal.pdf"),
    ]
    for case in cases:
        cut_pdf(case.input_path, case.output_path, case.ignore)


def check_case(case: Case):
    if case.wanted_path.exists():
        logger.info("assert for case {} {}", case.output_path, case.wanted_path)
        # TODO: hash compare is not a good solution
        return file_hash(case.output_path) == file_hash(case.wanted_path)
    return True


def file_hash(filepath, hash_func=hashlib.md5):
    hasher = hash_func()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):  # 逐块读取
            hasher.update(chunk)
    return hasher.hexdigest()


def test_bugfix_rotate() -> None:
    base = Path("cases/bugfix/rotate")
    cases = [Case(i) for i in base.files("*.pdf")]

    for case in cases:
        cut_pdf(case.input_path, case.output_path, case.ignore)
        check_case(case)
