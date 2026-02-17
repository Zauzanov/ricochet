import contextlib                                                           # Gives utilities for writing context managers. We use it to make chdir() work with 'with'.
import os                                                                   # os.walk() to traverse dirs; os.path helpers; os.getcwd()/chdir() to change dirs.
import queue                                                                # Thread-safe queues. queue.Queue() to safely share work/results between threads. 
import requests                                                             # Send GET reqs to the target server.
import sys                                                                  # Access to stdout.
import threading                                                            # Lets us spawn threads to run test_remote() concurrently.
import time                                                                 # Against throttling.

FILTERED = [".jpg", ".gif", ".png", ".css"]                                 # A list of file extensions we don’t want to test remotely.
TARGET = "http://localhost:8080"                                            # The target web server we are mapping. 
THREADS = 10                                                                # Number of worker threads to spawn for remote testing.

# Shared queues
answers = queue.Queue()                                                     # Where we store successful(200) URLs.
web_paths = queue.Queue()                                                   # This one holds all the paths we plan to test, think of it as a wordlist. 

def gather_paths():
    for root, _, files in os.walk('.'):
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith('.'):
                path = path[1:]
            print(path)
            web_paths.put(path)

@contextlib.contextmanager
def chdir(path):
    '''
    First, follow the specified path. 
    At the end, return to the original directory.
    '''
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = f'{TARGET}{path}'
        time.sleep(2)                              
        r = requests.get(url)
        if r.status_code == 200:
            answers.put(url)
            sys.stdout.write('+')
        else:
            sys.stdout.write('-')
        sys.stdout.flush()

def run():
    mythreads = list()
    for i in range(THREADS):
        print(f'Spawning thread {i}')
        t = threading.Thread(target=test_remote)
        mythreads.append(t)
        t.start()
    
    for thread in mythreads:
        thread.join()

if __name__ == '__main__':
    with chdir("/home/kali/Downloads/wordpress"):                       # Our local WP directory is functioning as a wordlist of potential web paths.
        gather_paths()
    input('Press return to continue.')

    run()
    with open('myanswers.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\n')
    print('done')