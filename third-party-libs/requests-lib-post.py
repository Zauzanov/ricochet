import requests

url = 'https://example.com'
data = {'user': 'tim', 'passwd': '31337'}
response = requests.post(url, data=data)            # POST request.
print(response.text)                                # response.text = string.
# print(response.content) — response.content = bytestring.                                                