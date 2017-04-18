import PyPDF2 as pdflib
from PyPDF2 import PdfFileWriter, PdfFileReader

pdf = PdfFileReader(file('input.pdf', 'rb'))
out = PdfFileWriter()

for page in pdf.pages:
  page.mediaBox.upperRight = (580,800)
  page.mediaBox.lowerLeft = (128,232)
  out.addPage(page)

ous = file('output.pdf', 'wb')
out.write(ous)
ous.close()