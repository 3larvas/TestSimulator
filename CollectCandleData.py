import json
import requests

url = "https://api.upbit.com/v1/candles/minutes/5?market=KRW-ETH&count=10"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

jsonObject = json.loads(response.text)
print(response.text)