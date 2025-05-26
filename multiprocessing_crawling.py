from multiprocessing import Process , Queue
import time 
from bs4 import BeautifulSoup
import re 
import requests
import random
import os     

# def print_time(thread_name, delay, iterations):
#     start = int(time.time())
#     for i in range(0, iterations):
#         time.sleep(delay)
#         seconds_elapsed = str(int(time.time()) - start)
#         print(thread_name if thread_name else seconds_elapsed)


# if __name__ == '__main__':

#     processes = []
#     processes.append(Process(target=print_time , args= ('Fizz', 3, 100)))
#     processes.append(Process(target=print_time , args= ('Buzz', 5, 100)))


#     for p in processes:
#         p.start()

#     for p in processes:
#         p.join()


# visited = []
# def getLinks (bs):
#     print(f"getting links in  {os.getpid()}")
#     links = bs.find('div' , {'id' : 'bodyContent'} ).find_all('a' , href = re.compile(r'^(/wiki/)((?!:).)*$'))
#     return [link for link in links if link not in visited]


# def scrape_article (path):
#     visited.append(path)
#     html = requests.get(f"http://en.wikipedia.org{path}")
#     bs = BeautifulSoup(html.text, 'html.parser')
#     title = bs.find('h1').get_text()    
#     print(f"scraping {title} in process {os.getpid()}")
#     links = getLinks(bs)

#     if len(links) > 0: 
#         newArticle = links[random.randint(0, len(links)-1)].attrs['href']
#         print(newArticle)
#         scrape_article(newArticle)


# if __name__ == '__main__':
#     processes = []
#     processes.append(Process(target=scrape_article , args=('/wiki/Kevin_Bacon',)))
#     processes.append(Process(target=scrape_article , args=('/wiki/Monty_Python',)))

#     for p in processes:
#         p.start()

#     for p in processes:
#         p.join()




#consumer producer pattern (one process append to the queue , while the other processes dequue the tasks )
def task_delegator (tasksQueue, urlsQueue):
    #initialize with a queue for each process 
    visited = ['/wiki/Kevin_Bacon', '/wiki/Monty_Python']
    tasksQueue.put('/wiki/Kevin_Bacon')
    tasksQueue.put('/wiki/Monty_Python')

    while True:
        #check if there are new link to process in the urlsQueue
        if not urlsQueue.empty():
            links = [link for link in urlsQueue.get() if link not in visited]

            for link in links:
                tasksQueue.put(link)
                visited.append(link)


def getLinks(bs):
    links = bs.find('div', {'id' : 'bodyContent'}).find_all('a', href = re.compile(r'^(/wiki/)((?!:).)*$'))
    return [link.attrs['href'] for link in links]


def scrape_article (tasksQueue, urlsQueue):
    while True:
        while tasksQueue.empty():
            time.sleep(0.1)  #wait for new task to be added 

        path = tasksQueue.get()
        html = requests.get(f'http://en.wikipedia.org{path}')
        bs = BeautifulSoup(html.text , 'html.parser')
        title = bs.find('h1').get_text()
        print(f"scraping {title} in process {os.getpid()}")
        links = getLinks(bs)
        
        #send links to the delegator 
        urlsQueue.put(links)

if __name__ == '__main__':

    processes = []
    tasksQueue = Queue()
    urlsQueue = Queue()

    processes.append(Process(target=task_delegator , args= (tasksQueue, urlsQueue))) #task delegator process 
    processes.append(Process(target=scrape_article , args= (tasksQueue, urlsQueue))) #scraper process 
    processes.append(Process(target=scrape_article , args= (tasksQueue, urlsQueue))) #scraper process 


    for p in processes:
        p.start()

    for p in processes:
        p.join()