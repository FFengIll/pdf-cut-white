from pypdf import PdfReader, PdfWriter
import pytest


@pytest.mark.skip()
def test_pypdf():
    output = PdfWriter()
    input1 = PdfReader(open("cases/input/input.pdf", "rb"))

    # print how many pages input1 has:
    print("document1.pdf has %d pages." % len(input1.pages))

    # add page 1 from input1 to output document, unchanged
    output.add_page(input1.getPage(0))

    # add page 2 from input1, but rotated clockwise 90 degrees
    output.add_page(input1.getPage(1).rotateClockwise(90))

    # add page 3 from input1, rotated the other way:
    output.add_page(input1.getPage(2).rotateCounterClockwise(90))
    # alt: output.add_page(input1.getPage(2).rotateClockwise(270))

    # add page 4 from input1, but first add a watermark from another PDF:
    page4 = input1.getPage(3)
    watermark = PdfReader(open("input.pdf", "rb"))
    page4.mergePage(watermark.getPage(0))
    output.add_page(page4)

    # add page 5 from input1, but crop it to half size:
    page5 = input1.getPage(4)
    page5.mediabox.upperRight = (
        page5.mediabox.getUpperRight_x() / 2,
        page5.mediabox.getUpperRight_y() / 2,
    )
    output.add_page(page5)

    # add some Javascript to launch the print window on opening this PDF.
    # the password dialog may prevent the print dialog from being shown,
    # comment the the encription lines, if that's the case, to try this out
    output.addJS("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")

    # encrypt your new PDF and add a password
    password = "secret"
    output.encrypt(password)

    # finally, write "output" to document-output.pdf
    outputStream = open("cases/output/output.pdf", "wb")
    output.write(outputStream)
