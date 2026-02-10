import requests

url = 'https://example.com'
response = requests.get(url)            # GET-request

print(response.text)