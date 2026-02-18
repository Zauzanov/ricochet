import queue
import requests
import threading
import sys 

AGENT = "Mozilla/5.0 (X11; Linux i686; U;rv: 1.7.13) Gecko/20070322 Kazehakase/0.4.4.1"
EXTENSTIONS = ['.php', '.bak', '.orig', '.inc']
TARGET = "http://localhost:8080"
THREADS = 50
WORDLIST = "/home/kali/Downloads/all.txt"

def get_words(resume=None):

    def extend_words(word):
        if "." in word:
            word.put(f'/{word}')
        else:
            word.put(f'/{word}/')
        
        for extension in EXTENSTIONS:
            word.put(f'/{word}{extension}')
    
    with open(WORDLIST) as f:
        raw_words = f.read()

    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')
        
        else:
            print(word)
            extend_words(word)
    return words 

