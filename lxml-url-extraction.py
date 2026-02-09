from io import BytesIO                                  # For working with streams(file-like objects). 
                                                        # BytesIO is an in-memory bytes buffer that behaves like a file opened in binary mode. 
from lxml import etree                                  # Provides parsing and tree APIs for XML/HTM.
import requests                                         # For HTTP calls.

url = 'https://example.com'
r = requests.get(url)                                   # Makes a GET-request to url, returning `requests.Response` object stored in `r`.
                                                        # Also inside r: r.status_code; r.headers; r.content(raw bytes); r.text(decoded string using an inferred encoding).

content = r.content                                     # `content` is a byte data type(avoids mistakes and easy to detect encoding for parser).

parser = etree.HTMLParser()                             # Creates an HTML parser instance. 
content = etree.parse(BytesIO(content), parser=parser)  # etree.parse() reads from the stream and parses it into an ElementTree object.
                                                        # etree.parse() likes to parse from a filename or a file-like object. 
                                                        # The HTTP response body is raw bytes, so BytesIO(content) wraps those bytes as a file-like stream.   
for link in content.findall('.//a'):                     # Finds all URLs: `//a` is an XPath expression to find every <a> tags in the doc.
    print(f"{link.get('href')} -> {link.text}")         # Prints the attibute value of href plus the direct text content inside the <a> tag. 