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