from io import BytesIO
from lxml import etree
import requests

url = "https://example.com"
r = requests.get(url, timeout=10)                       # Prevents from hanging forever.
r.raise_for_status()                                    # Checks the HTTP status code of a response to skip error pages. 

parser = etree.HTMLParser() 
tree = etree.parse(BytesIO(r.content), parser)          # Creates an ElementTree, representing the whole parsed doc.

for a in tree.xpath("//a"):                             # xpath() is more predictable than previous findall() with Xpath-like strings.
    href = a.get("href")                                # Get the href attribute.
    text = " ".join(a.itertext()).strip()               # Collects all text inside <a> including nested elements.
                                                        # itertext() yields text fragments: joins them and cleans whitespace.
    print(f"{href} -> {text}")                          # Prints the result in href + text format.
