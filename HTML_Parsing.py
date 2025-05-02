from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re

# html = urlopen('http://www.pythonscraping.com/pages/page1.html') #initiate TCP connection with the server 
# # print(html.read()) #this gets the raw html

# #parse hml using BeautifulSoup
# bs = BeautifulSoup(html.read(), 'html.parser') #provide html text and parser 
# print(bs.title)


#2 errors can occur when trying to connect to a web server
#server not found 
#page not found on the server 

# try:
#     html = urlopen('http://www.pythonscraping.com/pages/page1.html')

# except HTTPError as e: #page not found on the server 
#     print(e)

# except URLError as e:
#     print("Web server not found")

# #once the server connection is initiated the tag could not exist in that case we need to check 
# else:
#     bs = BeautifulSoup(html.read(), 'html.parser')
#     title = bs.find('h1')
#     if (title):
#         print(title)

#     else:
#         print("title not found")

#     #if we want to find a nested tag
#     try:
#         anothercontent = bs.nonexistingtag.anothertag
    
#     except AttributeError:
#         print("could find tag inside title")



# try:
#     html = urlopen('https://www.pythonscraping.com/pages/warandpeace.html')

# except HTTPError as e: #page not found on the server 
#     print(e)

# except URLError as e:
#     print("Web server not found")

# else:
#     bs = BeautifulSoup(html.read(), 'html.parser')

#     namelist = bs.find_all('span', {'class', 'green'})
#     for name in namelist:
#         print(name)



try:
    html = urlopen('https://www.pythonscraping.com/pages/page3.html')

except HTTPError as e: #page not found on the server 
    print(e)

except URLError as e:
    print("Web server not found")

else:
    bs = BeautifulSoup(html.read(), 'html.parser')
    print(bs.prettify())

    #find all children 
    # for child in bs.find('table', {'id': 'giftList'}).children:
    #     print(child)

    # for child in bs.find('table', {'id': 'giftList'}).tr.next_siblings: #exclude the current object 
    #     print(child)
        

    #rettriving parents
    # parent = bs.find('img', {'src':'../img/gifts/img1.jpg'}).parent.previous_sibling
    # print(parent)

    #using regular expression for string parsing 
    # images = bs.find_all('img', {'src': re.compile(r'\.\./img/gifts/img.*\.jpg')})
    # for image in images:
    #     print(image)

    #retrieving attributes 
    # table = bs.find('table', {'id': 'giftList'})
    # print(table['id'])