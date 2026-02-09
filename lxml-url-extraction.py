from io import BytesIO
from lxml import etree
import requests

url = 'https://example.com'
r = requests.get(url)                                   # GET-request.
content = r.content                                     # `content` is a byte data type.

parser = etree.HTMLParser()
content = etree.parse(BytesIO(content), parser=parser)  # Converts into a tree. 
for link in content.findall('//a'):                     # Finds all URLs — elements 'a'.
    print(f"{link.get('href')} -> {link.text}")