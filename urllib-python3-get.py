import urllib.parse
import urllib.request

url = 'https://example.com/'
with urllib.request.urlopen(url) as response: # GET
    content = response.read()

print(content)

