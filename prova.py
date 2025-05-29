import requests
from io import BytesIO
from pdfminer.high_level import extract_text_to_fp

def readPDF(pdfFile):
    retstr = BytesIO()
    extract_text_to_fp(pdfFile, retstr)
    content = retstr.getvalue().decode('utf-8')
    retstr.close()
    return content

pdf_response = requests.get('https://pythonscraping.com/pages/warandpeace/chapter1.pdf')
outputstring = readPDF(BytesIO(pdf_response.content))
print(outputstring)