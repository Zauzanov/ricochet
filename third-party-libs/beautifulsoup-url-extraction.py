from bs4 import BeautifulSoup as bs             # Imports the main parser/DOM wrapper class as an alias.
import requests

url = 'https://example.com'
r = requests.get(url)                           # Sends a GET-request to the URL.
'''
r is a requests.Response object that contains:
    r.status_code (200, 404 and so on)
    r.headers
    r.text (decoded string body)
    r.content (raw bytes body)
'''
tree = bs(r.text, 'html.parser')                # We tell bs which parser backend to use: 'html.parser' is Python’s built-in HTML parser. 
                                                # It parses the HTMK and builds a navigable structure of tags and text, the tree. 
for link in tree.find_all('a'):                 # Returns a list of all <a> tags. 
    print(f"{link.get('href')} -> {link.text}") # Fetches the href attribute from the <a> tag + returns all human-readable text inside the tag, as a string.