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


def dir_bruter(words):
    headers = {'User-Agent': AGENT}
    while not words.empty():
        url = f'{TARGET}{words.get()}'
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x');sys.stderr.flush()
            continue
        if r.status_code == 200:
            print(f'\nSuccess ({r.status_code}: {url})')
        elif r.status_code == 404:
            sys.stderr.write('.');sys.stderr.flush()
        else:
            print(f'{r.status_code} => {url}')


if __name__ == '__main__':
    words = get_words()
    print('Press return to continue.')
    sys.stdin.readline()
    for _ in range(THREADS):
        t = threading.Thread(target=dir_bruter, args=(words,))
        t.start()

