from PyPDF2 import PdfFileWriter, PdfFileReader

pdf = PdfFileReader(open('cases/input/input.pdf', 'rb'))
out = PdfFileWriter()

for page in pdf.pages:
    page.mediaBox.upperRight = (580, 800)
    page.mediaBox.lowerLeft = (128, 232)
    out.addPage(page)

ous = open('cases/output/output.pdf', 'wb')
out.write(ous)
ous.close()
