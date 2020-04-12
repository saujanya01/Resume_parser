import io
import PyPDF2 as ppdf
import tabula

import person_details

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

def to_text(filename):
    infoDict = {}
    info = info_pdf(filename)
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    print(filename+" in process text")
    with open("./static/"+filename, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()

    infoDict['person'] = person_details.extract(text)
    infoDict['pdf_details'] = info
    return infoDict

#for infpo_pdf
#flist = font list
#inum = number of images
#ntable = number of tables

def info_pdf(filename):
    file = open("./static/"+filename,"rb")
    pdfReader = ppdf.PdfFileReader(file)
    flist=[]
    inum=0
    for i in range(pdfReader.numPages):
        pg = pdfReader.getPage(i)
        if ('/XObject' in list(pg['/Resources'].keys())):
            inum = inum+len(pg['/Resources']['/XObject'].keys())
        for j in range(1,len(pg['/Resources']['/Font'].keys())):
            z = pg['/Resources']['/Font'][list(pg['/Resources']['/Font'].keys())[j]]['/BaseFont'][1:]
            if z not in flist:
                flist.append(z)
    file = "./static/"+filename
    tables = tabula.read_pdf(file, pages = "all", multiple_tables=True)
    ntable=len(tables)
    info = {}
    info['table_count'] = ntable
    info['fonts'] = flist
    info['image_count'] = inum
    return info