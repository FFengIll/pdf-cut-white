import loguru

from .cutter import cut_pdf, batch_cut_pdf
from .analyzer import analyse_area
logger = loguru.logger


def test_one():
    inputfile = './cases/input/input.pdf'
    outputfile = './cases/output/output.pdf'
    cut_pdf(inputfile, outputfile)


def test_batch():
    outdir = './cases/output'
    indir = './cases/input'
    batch_cut_pdf(indir, outdir)


def test_analyzer():
    analyse_area('test-complex2.pdf')


def tests():
    test_one()
    test_batch()
    
