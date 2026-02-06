import urllib2                                      # Python 2's HTTP client lib for opening URLs.

url = 'http://example.com'                          # URL we want to request.
headers = {'User-agent': 'Googlebot'}               # We specify our own headers. Web crawler used by Google to discover web pages.
request = urllib2.Request(url, headers=headers)     # We pass the URL and the dict to it. 
response = urllib2.urlopen(request)                 # Pass the new-established object to the func. Performs an HTTP request, GET by default. Returns a file-like response object.  
print(response.read())                              # Reads the entire response body from the server as bytes, then prints it.
response.close()                                    # Close the response and underlying socket to free resources.

