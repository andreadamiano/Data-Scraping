from urllib.error import HTTPError , URLError
from urllib.request import urlopen ,Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import random
import datetime
import time 

#connect to Wikipedia Web Page 
# try:
#     html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")

# except HTTPError as e:
#     print(e)

# except URLError:
#     print("Web server not found")

# else:
#     bs = BeautifulSoup(html.read(), "html.parser")
#     # print(bs.prettify()) #view html content 

#     for link in bs.find('div', {'id' : 'bodyContent'}).find_all('a', href = lambda href: href and href.startswith('/wiki/') and ':' not in href):
#         print(link.attrs['href'])

#     link
    
# random.seed(datetime.datetime.now().timestamp())
# def getLinks(articleURL):
#     try:
#         html = urlopen(f"https://en.wikipedia.org/{articleURL}")

#     except HTTPError as e:
#         print(e)

#     except URLError:
#         print("Web server not found")

#     else:
#         bs = BeautifulSoup(html.read(), "html.parser")
#         return bs.find('div', {'id' : 'bodyContent'}).find_all('a', href = lambda href: href and href.startswith('/wiki/') and ':' not in href) #return all the internal links 
    

# links = getLinks('/wiki/Kevin_Bacon')
# while len(links) >0:
#     newArticle = links[random.randint(0, len(links)-1)].attrs['href']
#     print(newArticle)
#     getLinks(newArticle)
#     time.sleep(2)
    


#web crawler 
# pages = set() #use an unordered list to store previously visited pages (fast lookups O(1))
# def getLinks(pageURL):
#     global pages

#     try:
#         html = urlopen(f"https://en.wikipedia.org/{pageURL}")

#     except HTTPError as e:
#         print(e)

#     except URLError:
#         print("Web server not found")

#     else:
#         bs = BeautifulSoup(html.read(), 'html.parser')

#         #fetch data 
#         try:
#             print(bs.h1.get_text())
#             print(bs.find(id ='mw-content-text').find_all('p')[0])
#             print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])
                  
#         except AttributeError:
#             print("This page is missingsomething, continue")



#         #crawl to the next web page 
#         for link in bs.find_all('a', href = lambda href: href and href.startswith('/wiki/')):
#             if 'href' in link.attrs:
#                 if link.attrs['href'] not in pages: #if not already visited 
#                     newPage =link.attrs['href']
#                     print(newPage)
#                     pages.add(newPage)
#                     time.sleep(1)
#                     getLinks(newPage)


# getLinks('')


#web crawler that travel across the internet
pages = set()
random.seed(datetime.datetime.now().timestamp())

#retrieve a list of internal links find in a page 
def getInternalLinks(bs, includeUrl):
    includeUrl = f'{urlparse(includeUrl).scheme}://{urlparse(includeUrl).netloc}' #parsing the url 
    internalLinks = []

    #find all lnks that begins with '/'
    for link in bs.find_all('a', href = lambda href: href and (href.startswith('/') or includeUrl in href)):
        if link.attrs['href'] not in internalLinks:
            if link.attrs['href'].startswith('/'):
                internalLinks.append(includeUrl + link.attrs['href'])

            else:
                internalLinks.append(link.attrs['href'])

    return internalLinks


#retrieve a list of external links
def getExternalLinks (bs, excludeUrl):
    externalLinks = []

    #find all links containing 'http' that do not contain the current url
    for link in bs.find_all('a' , href = lambda href: href and ((href.startswith('http') or href.startswith('www')) and excludeUrl not in href)):
        if link.attrs['href'] not in externalLinks:
            externalLinks.append(link.attrs['href'])

    return externalLinks


def getRandomExternalLinks(startingPage):
    req = Request(startingPage, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    bs = BeautifulSoup(html.read(), 'html.parser')
    externalLinks = getExternalLinks(bs, urlparse(startingPage).netloc)

    if len(externalLinks) ==0:
        print("no external lnks, looking around the site for one")

        domain = f'{urlparse(startingPage).scheme}://{urlparse(startingPage).netloc}'
        internalLinks = getInternalLinks(bs, startingPage)
        return getRandomExternalLinks(internalLinks[random.randint(0, len(internalLinks)-1)])
    
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]
    
def followExternaOnly(startingSite):
    externaLink = getRandomExternalLinks(startingSite)
    print(f'random external link is: {externaLink}')
    followExternaOnly(externaLink)

followExternaOnly('http://oreilly.com')