import os
import re
import PyPDF2

def find_pages(path, code):
    pdfFileObj = open(path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pages = list()

    for pageNo in range(pdfReader.getNumPages()):
        pageObj = pdfReader.getPage(pageNo)
        revInfo = pageObj.extractText()[123:135]
        if code in revInfo:
            pages.append(int(pageNo) + 1)
            
    pdfFileObj.close()
    
    return pages

if __name__=='__main__':
    path = r'C:\Users\Lenovo\Downloads\result.pdf'
    code = '058'
    pages = find_pages(path, code)
    print(pages)