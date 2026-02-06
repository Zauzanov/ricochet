import urllib.parse
import urllib.request

url = 'https://example.com/'
info = {'user': 'tim', 'passwd': '31337'}
data = urllib.parse.urlencode(info).encode()            # Encodes the dict with the creds into bytes.

req = urllib.request.Request(url, data)                 # Put the dict into the POST-request.
with urllib.request.urlopen(req) as response:           # POST-request and read the response. 
    content = response.read()

print(content)

'''
These `info` and `data` — they create a body like: user=tim&passwd=31337. This body can't exist in a GET-request, so the library switches to POST.
It's POST-request because data is not None. 
Also this request is POST because data is passed to Request(). If data were None, it would be GET: `req = urllib.request.Request(url, data=None)`
'''