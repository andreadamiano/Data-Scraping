from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen, Request
import time
import random

# class Content:
#     def __init__(self, url, title, body):
#         self.url = url
#         self.title = title
#         self.body = body

# #approach 1: write a web crawler specific for each website
# def getPage(url):
#     req = requests.get(url)
#     return BeautifulSoup(req.text, 'html.parser')
#     # req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})  # Mimic a browser
#     # html = urlopen(req)
#     return BeautifulSoup(html.read(), 'html.parser')


# def scrapeNYTimes(url):
#     bs = getPage(url)
#     title = bs.find('h1').text
#     lines = bs.find_all('p' , {'class' : 'story-content'})
#     body = '\n'.join([line.text for line in lines])
#     return Content(url, title, body)

# def scrapeBrookings(url):
#     bs = getPage(url)
#     title = bs.find('h1').text
#     body = bs.find('div' , {'class' : 'medium max-w-[540px] wysiwyg'}).text
#     return Content(url, title, body)

# #scrape Brookings
# url = 'https://www.brookings.edu/tags/future-development/'
# content = scrapeBrookings(url)
# print(f'Title: {content.title}')
# print(f'URL: {content.url}')
# print(content.body)

# #scapre NYTimes
# print('\n')
# url = 'https://www.nytimes.com/2018/01/25/opinion/sunday/'
# content = scrapeNYTimes(url)
# print(f'Title: {content.title}')
# print(f'URL: {content.url}')
# print(content.body)


# class Content:
    
#     def __init__(self, url, title, body):
#         self.url = url
#         self.title = title
#         self.body = body

#     def print(self):
#         print(f'Title: {self.title}')
#         print(f'URL: {self.url}')
#         print(f'Body:\n {self.body}')
        

# #stores info on how to estract data from the website 
# class Website:
#     def __init__(self, name, url, titleTag, bodyTag):
#         self.name = name 
#         self.url = url
#         self.titleTag = titleTag
#         self.bodyTag = bodyTag

# class Crawler:
#     def getPage(self, url):

#         """
#         utility function that gets the HTTP connection
#         """
#         try:
#             req = requests.get(url)

#         except requests.exceptions.RequestException:
#             return None
        
#         return BeautifulSoup(req.text, 'html.parser')


#     def safeGet(self, pageObj, selector):
#         """
#         utility function that helps get a content string from a bs object and a selector 
#         """ 

#         selectedElems = pageObj.select(selector)
#         if selectedElems is not None and len(selectedElems)>0:
#             return '\n'.join([elem.get_text() for elem in selectedElems])
        
#         else:
#             return ''
        
#     def parse(self, site, url):
#         bs = self.getPage(url)

#         if bs is not None:
#             title = self.safeGet(bs, site.titleTag)
#             body = self.safeGet(bs, site.bodyTag)
#             if title != '' and body != '':
#                 content = Content(url, title, body)
#                 content.print()
        

# crawler = Crawler()

# siteData = [
#     ['O\'Reilly Media', 'http://oreilly.com',
#     'h1', 'section#product-description'],
#     ['Reuters', 'http://reuters.com', 'h1',
#     'div.StandardArticleBody_body_1gnLA'],
#     ['Brookings', 'http://www.brookings.edu',
#     'h1', 'div[class*="wysiwyg-block"]'],
#     ['New York Times', 'http://nytimes.com',
#     'h1', 'p.story-content']
# ]

# websites = []
# for row in siteData:
#     websites.append(Website(row[0], row[1], row[2], row[3]))

# #test scraping brooklings
# crawler.parse(websites[2], 'https://www.brookings.edu/events/bloggers-buzz-and-soundbites-innovative-media-approaches-to-humanitarian-response/')   


class Content:
    """
    class to store web content 
    """
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print(f"New article found for topic: {self.topic}")
        print(F"Title: {self.title}")
        print(F"Body: {self.body}")
        print(F"Url: {self.url}\n")



class Website:
    """
    class to store website info 
    """
    def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name #website name
        self.url = url #website url 
        self.searchUrl = searchUrl #search url pattern (e.g., "https://www.amazon.com/s?k={query}")
        self.resultListing = resultListing #css selector for each result box 
        self.resultUrl = resultUrl #css selector for the link inside each result
        self.absoluteUrl=absoluteUrl #boolean: are links absolute or relative  
        self.titleTag = titleTag #css selector for title 
        self.bodyTag = bodyTag #css selctor for body 

#the crawler uses the search bar to get to other web pages 
class Crawler:
    def getPage(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.reuters.com/'
            }
            req = requests.get(url, headers= headers)

        except requests.exceptions.RequestException:
            return None
        
        return BeautifulSoup(req.text, 'html.parser')
    
    def safeGet (self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) >0:
            if isinstance(childObj, list):
                return [elem.get_text() for elem in childObj]

            else:
                return childObj[0].get_text() #return the first of the list 
        
        return ''
    
    def search(self, topic, site):
        """
        search a given website for a given topic and record all the pages found
        """

        bs = self.getPage(site.searchUrl + topic)
        searchReults = bs.select(site.resultListing)

        #loop trhough each result 
        for result in searchReults:
            url = result.select(site.resultUrl)[0].attrs['href'] #get the url of the result of the research 
            time.sleep(1)
            print(url)
            print('\n')

            #check if the url is an absolute or relative path 
            if site.absoluteUrl:
                bs = self.getPage(url)

            else:
                bs = self.getPage(site.url + url)

            if bs is None:
                print("Something went wrong with this page Url, skipping")
                return


            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)            

            if title != '' and body != '':
                content = Content(topic, url, title, body)
                content.print()



crawler = Crawler()

siteData = [
    ['Wikipedia', 'https://en.wikipedia.org',
    'https://en.wikipedia.org/wiki/Special:Search?search=',
    'div.mw-content-ltr.mw-parser-output li', 
    'a', 
    False, 
    'h1#firstHeading', 
    'div.mw-parser-output > p'
    ]
]


sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))


topics = ['python', 'data science']

for topic in topics:
    print(f"Getting info about: {topic}")
    crawler.search(topic, sites[0])