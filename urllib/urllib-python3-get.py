import urllib.parse
import urllib.request

url = 'https://example.com/'
with urllib.request.urlopen(url) as response:           # We use urlopen() as a context manager, making a GET-request, then reading it.
    content = response.read()

print(content)

