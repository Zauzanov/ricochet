import queue                                                                            # The thread-safe queue. Use it to store paths that multiple threads can safely consume.
import requests                                                                         # To sed GET requests to the target URL.
import threading                                                                        # To create multiple threads to do requests in parallel.
import sys                                                                              # Gives access to stdin/out/err. We use them to print progress markers and so on. 


# Some servers behave differently depending on User-agent, 
# so this makes our requests look like a browser:
AGENT = "Mozilla/5.0 (X11; Linux i686; U;rv: 1.7.13) Gecko/20070322 Kazehakase/0.4.4.1" # Choose any: https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/User-Agents/UserAgents.fuzz.txt
EXTENSTIONS = ['.php', '.bak', '.orig', '.inc']                                         # List of file extenstions to try for each word.
TARGET = "http://192.168.204.129/"                                                      # URL we are scanning. Every candidate path gets appended to this.
THREADS = 10                                                                            # Number of worker threads to spawn.
# File path to a wordlist containing candidate directory/file names:
WORDLIST = "/home/kali/Downloads/all.txt"                                               # Choose any from usr/share/wordlists/seclists/Discovery/web-content

# Builds and returns a Queue of paths to bruteforce
def get_words(resume=None):                                                             # `resume` let us restart mid-wordlist from a given word.
    
    def extend_words(word):                                                             # Inner helper function that takes a single word and enqueues multiple URL path variant.
        '''
        If the word already contains a dot(admin.php), it treats it like a file(/admin.php).
        Otherwise it treats like a dir(/admin/).
        '''
        if "." in word:
            words.put(f'/{word}') 
        else:
            words.put(f'/{word}/')
        
        for extension in EXTENSTIONS:                                                   # Tries the word(admin) as a file base name with each extenstion: /admin.bak, /admin.orig and so on. 
            words.put(f'/{word}{extension}')
    
    with open(WORDLIST) as f:
        raw_words = f.read()                                                            # Loads the wordlist, reading it into memory as one string.

    # Resume & queue building:
    found_resume = False                                                                # Tracks whether we've reached the resume point yet.
    words = queue.Queue()                                                               # The thread-safe queue that will hold all generated paths.
    for word in raw_words.split():                                                      # Splits the wordlist on whitespace and iterates each token.
        if resume is not None:                                                          # If resume was provided before resume word, it skips. Once we hit the resume word, it flips the flag and start adding subsequent words. 
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')
        # Normal mode(no resume):
        else:
            print(word)                                                                 # If resume isn't provided: print each word.
            extend_words(word)                                                          # Enqueues its variants via extent_words. 
    return words                                                                        # Returns the filled queue.


# Worker func run by each thread:
# consumes itmes from the queue and performs GET requests:
def dir_bruter(words):
    headers = {'User-Agent': AGENT}                                                     # Prepares the headers to send with every requests, using our custom UA.
    while not words.empty():                                                            # Loops until the queue appears empty.
        url = f'{TARGET}{words.get()}'                                                  # Removes one path from the queue, building full URL: TARGET+/admin/.
        try:
            r = requests.get(url, headers=headers)                                      # Sends a GET request.
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x');sys.stderr.flush()                                    # If connection fails(host down/refused), it prints x to stderr.
            continue
        # Status code handling: 
        if r.status_code == 200:                                                        # If HTTP 200 OK: likely found something.
            print(f'\nSuccess ({r.status_code}: {url})')                                # Prints a newline first, so the success does'nt get buried in dots.
        elif r.status_code == 404:
            sys.stderr.write('.');sys.stderr.flush()                                    # If 404 Not Found, prints a dot to stderr. Flushes so we see it immediately.
        else:
            print(f'{r.status_code} => {url}')                                          # For anything else(301 redirect, 403 forbiddeg, 500 error and so on).


if __name__ == '__main__':
    resume = sys.argv[1] if len(sys.argv) > 1 else None
    words = get_words(resume=resume)                                                    # Builds the queue using the wordlist.
    print('Press return to continue.')                                                  # Pauses until we press Enter.
    sys.stdin.readline()                                                                # Does nothing until we press Enter.
    # The loop index isn't used, as we don't care about this value:
    for _ in range(THREADS):                                                            # Spawns THREADS worker threads. 
        t = threading.Thread(target=dir_bruter, args=(words,))                          # The loop runs 10 times and starts 10 threads — each thread runs dir_bruter(words). 
        t.start()

# get_words() create the work(the queue full of paths);
# dir_bruter(words) consumes the work ( takes imes out of the queue and sends requests).

