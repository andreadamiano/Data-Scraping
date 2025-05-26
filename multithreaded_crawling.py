# import _thread
import threading
import time 
# from mysql.connector import Connect, Error
# import re
# from bs4 import BeautifulSoup
# import requests
# import random
# from queue import Queue


# def print_time(threadName, delay, iterations):
#     start = int(time.time())
#     for i in range (0, iterations):
#         time.sleep(delay)
#         second_elapsed = str (int(time.time() - start))
#         print(f"{second_elapsed} {threadName}")


# try:
#     _thread.start_new_thread(print_time , ('Fizz', 3 , 10))  #pass argument as a tuple 
#     _thread.start_new_thread(print_time , ('Buzz', 5 , 10))


# except:
#     print('unabe to start threads')



# #keep the main thread alive 
# while 1:
#     pass



# print_time(None, 3, 10)

# visited = []
# def getLinks(thread_name, bs):
#     print(f'getting link from {thread_name}')
#     links = bs.find('div', {'id' : 'bodyContent'}).find_all('a' , href = re.compile('^(/wiki/)((?!:).)*$'))
#     return [link for link in links if link not in visited]


# #define a function that will be executed by each thread 
# def scrape_article(thread_name, path):
#     visited.append(path)
#     html = requests.get( f'http://en.wikipedia.org{path}')
#     bs = BeautifulSoup(html.text , 'html.parser')
#     title = bs.find('h1').get_text()
#     print(f'scraping {title} in thread {thread_name}')
#     links = getLinks(thread_name, bs)
 
#     if len(links) > 0:   #if any link was found
#         newArticle = links[random.randint(0, len(links))].attrs['href']
#         print(newArticle)
#         scrape_article(thread_name, newArticle)


# #spawn 2 threads 
# try:
#     _thread.start_new_thread(scrape_article, ('Thread 1', '/wiki/Kevin_Bacon'))
#     _thread.start_new_thread(scrape_article, ('Thread 2', '/wiki/Monty_Python'))

# except:
#     print('Error, unable to start a new thread')


# #keep alive the main thread 
# while 1:
#     pass


# #this will handle the database connection
# def storage (queue):
#     with Connect(
#         host = "localhost", 
#         user =  input('User: '),
#         password = getpass(), 
#         database = 'wikipedia'
#     )as connection:
#         print("successfully connected")

#         with connection.cursor() as cursor:

#             #keep the thread alive 
#             while 1:
#                 if not queue.empty():
#                     article = queue.get()
#                     #check if the path already exists 
#                     cursor.execute(
#                         """
#                         select * from pages where path = %s
#                         """, (article['path'], )
#                     )
#                     result = cursor.fetchone()

#                     if result is None:
#                         print(f"storing article {article['path']}")
#                         cursor.execute(
#                             """
#                             insert into pages (title, path) values (%s, %s)
#                             """ , (article['title'], article['path'])
#                         )
#                         connection.commit()
#                     else:
#                         print(f"article already exists: {article['path']}")




# visited = []
# def getLinks(thread_name, bs):
#     print(f"getting links in {thread_name}")
#     links = bs.find('div',{'id': 'bodyContent'} ).find_all('a' , href =  re.compile(r'^(/wiki/)((?!:).)*$'))
#     return [link for link in links if link not in visited]


# def scrape_article(thread_name, path, queue):
#     html = requests.get(f"http://en.wikipedia.org{path}")
#     bs = BeautifulSoup(html.text, 'html.parser')
#     title = bs.find('h1').get_text()
#     print(f"added {title} for storage in thread {thread_name}")
#     queue.put({'title': title , 'path' : path})
#     links = getLinks(thread_name, bs)

#     if len(links) > 0: #if any link was found
#         newArticle = links[random.randint(0, len(links)-1)].attrs['href']
#         scrape_article(thread_name, newArticle, queue)


# #define a queue to comunicate between threads (in python is thread safe)
# queue = Queue()

# try:
#     _thread.start_new_thread(scrape_article, ('Thread 1' , '/wiki/Kevin_Bacon', queue))
#     _thread.start_new_thread(scrape_article, ('Thread 2' , '/wiki/Monty_Python', queue))
#     _thread.start_new_thread(storage, (queue,))

# except:
#     print('unable to start threads')

 

# #keep the main thread alive 
# while 1:
#     pass 



# def print_time(thread_name, delay, iterations):
#     start = int(time.time())
#     for i in range (0, iterations):
#         time.sleep(delay)
#         second_elapsed = str(int(time.time()) - start)
#         print(f"{second_elapsed} {thread_name}")


# # threading.Thread(target=print_time, args=('Fizz' , 3, 10)).start()
# # threading.Thread(target=print_time, args=('Buzz' , 5, 10)).start()

# t1 = threading.Thread(target=print_time, args=('Fizz', 3, 10), daemon=False)
# t2 = threading.Thread(target=print_time, args=('Buzz', 5, 10), daemon=False)
# t1.start()
# t2.start()


# def crawler(url):
#     data = threading.local()  #create a local object for each thread    
#     data.visited = []
#     print(f"Crawling {url}")


# t = threading.Thread(target= crawler , args= ('http://brookings.edu',))
# t.start()

# while 1:
#     time.sleep(3)
#     if not t.is_alive():  #check if the thread is alive 
#        t = threading.Thread(target= crawler , args= ('http://brookings.edu', )) #start a new thread 
#        t.start()


class Crawler (threading.Thread):
    def __init__(self):
        super().__init__()
        self.done = False
    
    def isDone(self):
        return self.done
    
    def run(self):  #will be called by the thread 
        print('function called')
        time.sleep(5)
        self.done = True
        raise Exception('something bad has happened')
    


t = Crawler()
t.start()


while True:
    time.sleep(1)
    if t.isDone():
        print('Done')
        break

    if not t.is_alive():
        t = Crawler()
        t.start()