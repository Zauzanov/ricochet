from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys 
import threading
import time

SUCCESS = 'Welcome to WordPress!'
TARGET = "http://localhost:8080/wp-login.php"
WORDLIST = "/home/kali/Downloads/cain-and-abel.txt" 

def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()
    
    words = Queue()

    for word in raw_words.split():
        words.put(word)
    return words

