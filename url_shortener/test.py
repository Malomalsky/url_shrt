import requests

url = "http://127.0.0.1:5000/add_link"

payload = "{\r\n    \"original_url\": \"ya.ru\", \r\n    \"custom_url\": \"\"\r\n}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))