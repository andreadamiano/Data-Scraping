# import requests
import json
from curl_cffi import requests
from bs4 import BeautifulSoup
import datetime
import random
import re

# response = requests.get('http://example.com/comments?post=123')
# print(response)





# headers = {
#     "User-Agent": "Mozilla/5.0",
#     "Accept": "application/json",
#     "Accept-Language": "it-IT,it;q=0.9",
#     "Referer": "https://www.adidas.it/",
# }

# session = requests.Session()
# session.get("https://www.adidas.it/", headers=headers) #get cookies 


# response = requests.get('https://www.adidas.it/plp-app/api/search?q=scarpe&experiment=ATP-6806-1%2CAT', impersonate='chrome')
# print(response.status_code)
# print(response.json())


random.seed(int (datetime.datetime.now().timestamp()))

def getLinks(articleUrl):
    html = requests.get(f'http://en.wikipedia.org{articleUrl}')
    bs = BeautifulSoup(html.text , 'html.parser')
    return bs.find('div', {'id' : 'bodyContent'}).find_all('a', href = re.compile(r'^(/wiki/)((?!:).)*$'))


def getHistory(pageUrl):
    pageUrl = pageUrl.replace('/wiki/' , '')  #remove wiki from the string
    historyUrl = f'https://en.wikipedia.org/w/index.php?title={pageUrl}&action=history'
    print(f'history Url: {historyUrl}')
    html = requests.get(historyUrl)
    bs = BeautifulSoup(html.text, 'html.parser')

    ipAddresses = bs.find_all('a', {'class' : 'mw-anonuserlink'})
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())
    
    return addressList


def getCountry(ipAddress):
    # headers = {'User-Agent': 'Mozilla/5.0'}
    # response = requests.get(f'https://ipapi.co/{ipAddress}/json/' , headers=headers)
    response = requests.get(f'https://ipinfo.io/{ipAddress}/json' ,impersonate= 'chrome')
    # print(response.json())
    responseJson = response.json()
    
    return responseJson.get('country')


links = getLinks('/wiki/Python_(programming_language)')


while len(links) >0:
    for link in links:
        print('-' * 20)
        historyIPs = getHistory(link.attrs['href'])
        for historyIP in historyIPs:
            country = getCountry(historyIP)
            print(f"{historyIP} from :{country}")


    newLink = links [random.randint(0, len(links)-1)]
    links = getLinks(newLink)

