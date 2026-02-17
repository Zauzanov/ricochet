import contextlib 
import os 
import queue 
import random                                                           # To randomize sleep time
import requests 
import sys
import threading
import time
from queue import Empty                                                 # Exception raised by Queue.get_nowait() when the queue is empty.
from urllib.parse import urljoin                                        # Correctly join base URL + path (handles slashes safely).

FILTERED = {".jpg", ".gif", ".png", ".css"}
TARGET = "http://localhost:8080"
THREADS = 10

answers = queue.Queue()
web_paths = queue.Queue()


def gather_paths():
    for root, _, files in os.walk("."):
        for fname in files:
            if os.path.splitext(fname)[1].lower() in FILTERED:
                continue

            path = os.path.join(root, fname)

            # Strip leading: './wp-content/...' becomes '/wp-content/...'
            if path.startswith("."):
                path = path[1:]

            # Normalizes to URL separators.
            path = path.replace(os.sep, "/")

            web_paths.put(path)


@contextlib.contextmanager
def chdir(path):
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)


def test_remote():
    # One session per thread.
    session = requests.Session()

    while True:
        try:
            path = web_paths.get_nowait()
        except Empty:
            return

        url = urljoin(TARGET.rstrip("/") + "/", path.lstrip("/"))

        time.sleep(0.2 + random.random() * 0.4)

        try:
            r = session.get(url, timeout=5)
            if r.status_code == 200:
                answers.put(url)
                sys.stdout.write("+")
            else:
                sys.stdout.write("-")
        except requests.RequestException:
            sys.stdout.write("!")
        finally:
            sys.stdout.flush()
            web_paths.task_done()


def run():
    threads = []
    for i in range(THREADS):
        t = threading.Thread(target=test_remote, daemon=True)
        threads.append(t)
        t.start()

    web_paths.join()


if __name__ == "__main__":
    with chdir("/home/kali/Downloads/wordpress"):
        gather_paths()

    input("Press return to continue.")
    run()

    with open("myanswers.txt", "w") as f:
        while not answers.empty():
            f.write(f"{answers.get()}\n")

    print("\ndone")
