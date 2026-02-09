from bs4 import BeautifulSoup as bs
import requests

url = 'https://example.com'
r = requests.get(url)
tree = bs(r.text, 'html.parser')                # Converts into a tree. 
for link in tree.find_all('a'):                 # Finds all <a> tags.
    print(f"{link.get('href')} -> {link.text}")