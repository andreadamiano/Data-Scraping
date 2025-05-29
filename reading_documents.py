import requests
from bs4 import BeautifulSoup
from io import StringIO, open , BytesIO
import csv 
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from zipfile import ZipFile

#parsing text file : use different econding (ISO, UTF-8, ASCII) 


# response = requests.get('https://pythonscraping.com/pages/warandpeace/chapter1-ru.txt')
# response.encoding = 'utf-8'  #specify the encoding 
# print(response.text)

# #find the encoder in html pages 
# html = requests.get('https://en.wikipedia.org/wiki/Python_(programming_language')
# bs = BeautifulSoup(html.text, 'html.parser')

# #get encoder
# encoder = bs.find('meta').attrs['charset']

# #get body 
# content = bs.find('div' , {'id' : 'mw-content-text'}).get_text()
# content = content.encode(encoder)

# print(content)



# #csv files 
# data = requests.get('http://pythonscraping.com/files/MontyPythonAlbums.csv')

# #decode content 
# data = data.content.decode('ascii')

# dataFile = StringIO(data)  #RAM file 

# for row in list(csv.DictReader(dataFile)): #csv reader return an iterator   
#     print(row)



# #pdf files 
# def readPDF (pdfFile):
#     buffer = BytesIO() #RAM file

#     laparams = LAParams() #preserve layout

#     #extract texti from PDF 
#     extract_text_to_fp(pdfFile, buffer ,laparams=laparams)

#     #fetch content
#     content = buffer.getvalue().decode('utf-8')
    
#     #close the RAM file
#     buffer.close()

#     return content


# pdfFile = requests.get('https://pythonscraping.com/pages/warandpeace/chapter1.pdf')
# outputstring = readPDF(BytesIO(pdfFile.content))
# print(outputstring)
# pdfFile.close() 


#.docx file (which is just a zip file containing XML files)
wordFile = requests.get('http://pythonscraping.com/pages/AWordDocument.docx')
wordFile = BytesIO(wordFile.content)
document = ZipFile(wordFile)  #unzip file 
xml_content = document.read('word/document.xml') #get xml content 

#parse XML
bs = BeautifulSoup(xml_content.decode('utf-8'), 'xml')
content = bs.find_all('w:t')

for element in content:
    print(element.text)