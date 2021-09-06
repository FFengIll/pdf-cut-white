import loguru

from .cutwhite import cut_white, batch

logger = loguru.logger


def test_one():
    inputfile = './input/input.pdf'
    outputfile = './output/output.pdf'
    cut_white(inputfile, outputfile)


def test_batch():
    outdir = './output'
    indir = './input'
    batch(indir, outdir)


def tests():
    test_one()
    test_batch()
