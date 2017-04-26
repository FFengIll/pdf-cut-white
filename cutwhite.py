import PyPDF2 as pdflib
from PyPDF2 import PdfFileWriter, PdfFileReader

import miner
import os, sys

def cut_box(box, res):
    """
    cut the box by setting new position (relative position)
    """
    (x1, y1, x2, y2) = res

    #must translate relative position to absolute position
    bx, by = box.getLowerLeft()
    bx=float(bx);by=float(by)

    print "origin:", box
    box.lowerLeft = (bx + x1, by + y1)
    box.upperRight = (bx + x2, by + y2)

def cut_white(inputname, outputname='output.pdf'):
    """
    cut the white slide of the input pdf file, and output a new pdf file
    """
    indata = PdfFileReader(file(inputname, 'rb'))
    outdata = PdfFileWriter()

    #get the visible area of the page, aka the box scale. res=[(x1,y1,x2,y2)]
    pageboxlist = miner.mine_area(inputname)

    num = indata.getNumPages()
    for i in range(num):
        scale = pageboxlist[i]
        page = indata.getPage(i)
        print scale

        cut_box(page.mediaBox, scale)
        # cut_box(page.trimBox,scale)
        # cut_box(page.artBox,scale)
        # cut_box(page.cropBox,scale)
        # cut_box(page.bleedBox,scale)
        outdata.addPage(page)

    output = file(outputname, 'wb')
    outdata.write(output)
    output.close()


def scan_files(directory, prefix=None, postfix=None, sub=False):
    """
    scan files under the dir with spec prefix and postfix
    """
    files_list = []

    for root, dirs, files in os.walk(directory):
        # print root, dirs, files
        for f in files:
            if postfix:
                if f.endswith(postfix):
                    files_list.append(os.path.join(root, f))
            elif prefix:
                if f.startswith(prefix):
                    files_list.append(os.path.join(root, f))
            else:
                files_list.append(os.path.join(root, f))
        if not sub:
            break

    return files_list


def batch_action(indir, outdir):
    files = scan_files(indir, postfix='pdf')
    print files

    for f in files:
        name = f.replace(indir, '')
        path = outdir + name

        print f
        print name
        print path

        id = path.rfind('\\')
        dir = path[:id]
        print dir

        if not os.path.exists(dir):
            os.makedirs(dir)
        cut_white(f, path)

def run_tests():
    inputfile = './input/input.pdf'
    inputfile = 'F:\\pdf\\dist\\concolic\\concolic2.pdf'
    inputfile = 'F:\\pdf\\dist\\concolic\\output\\output.pdf'
    outputfile = './output/output.pdf'
    outputfile = 'F:\\pdf\\dist\\concolic\\output\\output2.pdf'
    cut_white(inputfile, outputfile)
    exit(0)

    outdir = './output'
    indir = './input'
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    batch_action(indir, outdir)

if __name__ == "__main__":
    run_tests()
