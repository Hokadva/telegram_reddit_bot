import requests

URL = 'https://api.thecatapi.com/v1/images/search'
response = requests.get(URL).json()

print(response)