import datetime
import requests
import json
import slack_dir.SendMessage

term = 5
coin_nm = 'ETH'
url = 'https://api.upbit.com/v1/candles/minutes/'+str(term)+'?market=KRW-'+coin_nm+'&count=4'
headers = {"Accept": "application/json"}
response = requests.request("GET", url, headers=headers)
cur_data = json.loads(response.text)

def CheckDown() :
    # print(datetime.datetime.now())
    # for data in cur_data:
    #     print(data)
    #     if data['opening_price'] < data['trade_price']:
    #         print(f'opening : {data["opening_price"]}, > closing : {data["trade_price"]}')
    #         return
    # print('find down position!!')
    slack_dir.SendMessage.post_message('find down position!!')


CheckDown()