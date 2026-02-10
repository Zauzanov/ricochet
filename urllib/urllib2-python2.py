import urllib2                                      # Python 2's HTTP client lib for opening URLs.

url = 'http://example.com'                          # URL we want to request.
response = urllib2.urlopen(url)                     # Performs an HTTP request, GET by default. Returns a file-like response object.  
print(response.read())                              # Reads the entire response body from the server as bytes, then prints it.
response.close()                                    # Close the response and underlying socket to free resources.