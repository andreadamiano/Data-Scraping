import requests
from bs4 import BeautifulSoup
import re 
import string
from collections import Counter


# def getNGrams(content, n):

#     content = content.split(' ')
#     output = []

#     for i in range (len(content) -1):
#         output.append(content[i:i+n])
    
#     return output


# html = requests.get('http://en.wikipedia.org/wiki/Python_(programming_language)')
# bs = BeautifulSoup(html.text, 'html.parser')
# content = bs.find('div', {'id' : 'mw-content-text'}).get_text()
# # print(content)
# ngrams = getNGrams(content, 2)

# print(ngrams)
# print(f"r grams counnt {len(ngrams)}")


# def getNGrams(content, n):
#     content = re.sub(r'\n|\[\d+\]', ' ', content) #remove escapes characters or [1] values
#     content = content.encode('utf-8').decode('ascii', 'ignore') #remove non-ascii characters
#     content = content.split(' ')
#     output = []

#     for i in range(len(content)-n+1):
#         output.append(content[i:i+n])

#     return output


# html = requests.get('http://en.wikipedia.org/wiki/Python_(programming_language)')
# bs = BeautifulSoup(html.text, 'html.parser')
# content = bs.find('div', {'id' : 'mw-content-text'}).get_text()
# # print(content)
# ngrams = getNGrams(content, 2)
# print(ngrams)
# print(f"r grams counnt {len(ngrams)}")


def cleanSentence(sentence):
    sentence = sentence.split(' ')
    sentence = [word.strip(string.punctuation + string.whitespace)  for word in sentence]
    sentence = [word for word in sentence if len(word) > 1 or (word.lower() == 'a' or word.lower() == 'i')] #strip words from a sentence

    return sentence


def cleanInput(content):
    content = re.sub(r'\n|\[\d+\]', ' ', content)
    # print(content)
    content = content.encode('utf-8').decode('ascii', 'ignore')
    sentences = content.split('.')
    return [cleanSentence(sentence) for sentence in sentences ]

def getNgramsFromSentence(sentence, n):
    output = []
    for i in range(len(sentence) -n +1):
        output.append(sentence[i:i+n])
    return output

# def getNgrams(content, n):
#     content = cleanInput(content)
#     ngrams = []
#     for sentence in content:
#         ngrams.extend(getNgramsFromSentence(sentence, n))

#     return ngrams   

# data normalization (include frequencies and store ngrams only once)
def getNgrams(content, n):
    content = content.lower()
    content = cleanInput(content)
    ngrams = Counter()
    for sentence in content:
        newNgrams = [' '.join(ngrams) for ngrams in getNgramsFromSentence(sentence, n)]
        ngrams.update(newNgrams)

    return ngrams   


html = requests.get('http://en.wikipedia.org/wiki/Python_(programming_language)')
bs = BeautifulSoup(html.text, 'html.parser')
content = bs.find('div', {'id' : 'mw-content-text'}).get_text()
ngrams = getNgrams(content, 2)
print(ngrams)




