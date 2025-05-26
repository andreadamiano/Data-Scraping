# import os
import requests
# from urllib.request import urlretrieve
from bs4 import BeautifulSoup
# import csv
# import pandas as pd
import datetime 
import random
import re 
from mysql.connector import connect, Error
from getpass import getpass

# #get html
# html = requests.get('http://www.pythonscraping.com')
# bs = BeautifulSoup(html.text, 'html.parser')

# #find image
# image_url = bs.select_one('img[alt="python-logo"]')['src']

# #save image
# urlretrieve(image_url, 'logo.jpg')


# downloadDirectory = 'downloaded'
# baseUrl = 'https://pythonscraping.com/'

# def getAbsolutePath(baseUrl, source):

#     if source.startswith(baseUrl):
#         return source

#     elif source.startswith('https://www.'):
#         url = f"https://{source[12:]}"

#     elif source.startswith('www.'):
#         url = f"https://{source[4:]}"

#     else:
#         url = f"{baseUrl}/{source}"

#     if baseUrl not in source: #discard external links (potentially dangerous)
#         return None

#     return url



# def getDownloadPath (absoluteUrl, downloadDirectory):
#     filename = os.path.basename(absoluteUrl.split('?')[0]) #extract the file name
#     path = downloadDirectory + '/' + filename

#     return path

# if not os.path.exists(downloadDirectory):
#     os.makedirs(downloadDirectory)

# html = requests.get(baseUrl)
# bs = BeautifulSoup(html.text, 'html.parser')
# downloadList = bs.find_all(src=True) #get all embedded content in the website

# for download in downloadList:
#     fileUrl = download['src']
#     fileUrl = getAbsolutePath(baseUrl ,download['src'])
#     if fileUrl is not None:
#         print(fileUrl)
#         urlretrieve(fileUrl, getDownloadPath(fileUrl, downloadDirectory))



# html = requests.get('https://en.wikipedia.org/wiki/Comparison_of_text_editors')
# bs = BeautifulSoup(html.text, 'html.parser')

# #get comparison table
# table = bs.find('table', {'class' : 'wikitable'})

#easier way with pandas 
# df = pd.read_html(str(table))[0]  # [0] gets first table from the HTML string

# # Save to CSV
# df.to_csv('text_editors_comparison.csv', index=False)


#harder way with csv 
# rows = table.find_all('tr')
# with open('text_editors_comparison.csv', 'w', encoding='utf-8', newline='') as csvFile:
#     writer = csv.writer(csvFile)

#     for row in rows:
#         csvRow = []
#         for cell in row.find_all(['td', 'th']): #ifnd both regular cells and header cells 
#             csvRow.append(cell.get_text().strip())
        
#         writer.writerow(csvRow)

# random.seed(datetime.datetime.now().timestamp())

# def store(title, content):
#     cursor.execute("INSERT INTO pages (title, content) VALUES" "(%s, %s)" , (title, content))
#     connection.commit()


# def getLinks(articleUrl):
#     html = requests.get('http://en.wikipedia.org' + articleUrl)
#     bs = BeautifulSoup(html.text, 'html.parser')
#     title = bs.find('h1').get_text()
#     paragraphs = bs.find('div', {'id': 'mw-content-text'}).find_all('p')
#     content = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

#     store(title, content[:min(len(content)-1, 10000)])
#     return bs.find('div', {'id' : 'bodyContent'}).find_all('a', href = re.compile(r"^(/wiki/).*"))


# try:
#     with connect(
#         host = "localhost", 
#         user =  input('User: '),
#         password = getpass(),
#         database = 'data_scraping'
#     )as connection:
#         print("connected successfully")

#         with connection.cursor() as cursor:

#             links = getLinks('/wiki/Kevin_Bacon') #initial page url 

#             while(len(links)> 0):
#                 newArticle = links[random.randint(0 , len(links)-1)].attrs['href']
#                 print(newArticle)

#                 links = getLinks(newArticle)


# except Error as  e:
#     print(e)



#connect to the mysql server 

def insertPage(url):
    cursor.execute(
        """
        select *  
        from pages 
        where url = %s 
        """
        , (url,)
    )
    #fetch result
    result = cursor.fetchone()

    if result is None:  #if the url doesnt exists 
        cursor.execute(
            """
            insert into pages (url) values (%s)
            """
            , (url,)
        )
        connection.commit()
        return cursor.lastrowid  #return the last id 
    
    else:
        return result[0]  #returning the id of the existing page 

def loadPages():
    cursor.execute(
        """
        select * from pages
        """
    )
    pages = [ page[1]  for page in cursor.fetchall()]  #1 is the url 
    return pages 

def insertLink(fromPageID, toPageId):
    cursor.execute(
        """
        select * from links
        where fromPageId = %s and toPageId = %s
        """, (int(toPageId), int(fromPageID))
    )
    result = cursor.fetchone()
    if result is None:  #if the link doesnt exist inthe server  
        cursor.execute(
            """
            insert into links (fromPageId, toPageId) values (%s, %s)
            """, (int(fromPageID), int(toPageId))
        )
        connection.commit()
        return cursor.lastrowid  #return the last id 
    
    else:
        return result[0]

def getLinks(pageUrl, recursionLevel, pages):
    if recursionLevel > 4:
        return
    
    pageId = insertPage(pageUrl)
    html = requests.get(f'http://en.wikipedia.org{pageUrl}')
    bs = BeautifulSoup(html.text, 'html.parser')
    links = bs.find_all('a', href = re.compile(r'^(/wiki/)((?!:).)*$') )
    links = [link.attrs['href'] for link in links]
    
    #crawl 
    for link in links:
        insertLink(pageId, insertPage(link))

        if link not in pages: #get all the pages we have already crawled 
            print(link)
            pages.append(link)

            #recurse 
            getLinks(link, recursionLevel+1, pages)


    




with connect(
    host = 'localhost',
    user =  input('User: '),
    password = getpass(),
    database = 'wikipedia'
) as connection:
    print('successfully connected')

    with connection.cursor() as cursor:
        # insertPage('/wiki/Kevin_Bacon')
        # insertLink(0,1)
        getLinks('/wiki/Kevin_Bacon',0, loadPages())



