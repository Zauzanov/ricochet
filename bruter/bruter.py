import queue
import requests
import threading
import sys 

AGENT = "Mozilla/5.0 (X11; Linux i686; U;rv: 1.7.13) Gecko/20070322 Kazehakase/0.4.4.1"
EXTENSTIONS = ['.php', '.bak', '.orig', '.inc']
TARGET = "http://localhost:8080"
THREADS = 50
WORDLIST = "/home/kali/Downloads/all.txt"

