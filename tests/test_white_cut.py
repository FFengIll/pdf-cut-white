import loguru

import sys

sys.path.append(".")

from pdf_white_cut.cutter import cut_pdf, batch_cut_pdf
from pdf_white_cut.analyzer import analyse_pdf

logger = loguru.logger


def test_cut_pdf():
    inputfile = "./cases/input/input.pdf"
    outputfile = "./cases/output/output.pdf"
    cut_pdf(inputfile, outputfile)


def test_batch_cut_pdf():
    outdir = "./cases/output"
    indir = "./cases/input"
    batch_cut_pdf(indir, outdir)


def test_analyzer():
    analyse_pdf("test-complex2.pdf")


def test_rw_pdf():
    from PyPDF2 import PdfFileWriter, PdfFileReader

    pdf = PdfFileReader(open("cases/input/input.pdf", "rb"))
    out = PdfFileWriter()

    for page in pdf.pages:
        page.mediaBox.upper_right = (580, 800)
        page.mediaBox.lower_left = (128, 232)
        out.add_page(page)

    ous = open("cases/output/output.pdf", "wb")
    out.write(ous)
    ous.close()
