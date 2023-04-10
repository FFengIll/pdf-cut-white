import sys

import loguru
from pypdf import PdfReader, PdfWriter

sys.path.append(".")

from pdf_white_cut.analyzer import extract_pdf_boxs
from pdf_white_cut.cutter import batch_edit_pdf, edit_pdf

logger = loguru.logger


def test_cut_pdf():
    inputfile = "./cases/input/input.pdf"
    outputfile = "./cases/output/output.pdf"
    edit_pdf(inputfile, outputfile)


def test_batch_cut_pdf():
    outdir = "./cases/output"
    indir = "./cases/input"
    batch_edit_pdf(indir, outdir)


def test_analyzer():
    extract_pdf_boxs("test-complex2.pdf")


def test_rw_pdf():
    pdf = PdfReader(open("cases/input/input.pdf", "rb"))
    out = PdfWriter()

    for page in pdf.pages:
        page.mediabox.upper_right = (580, 800)
        page.mediabox.lower_left = (128, 232)
        out.add_page(page)

    ous = open("cases/output/output.pdf", "wb")
    out.write(ous)
    ous.close()
