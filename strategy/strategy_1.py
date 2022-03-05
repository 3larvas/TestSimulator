import json
import requests
# 변동성 돌파 전략

term = 30
K = 0.5
coin_nm = 'ETH'

# 변동폭 계산
url = 'https://api.upbit.com/v1/candles/minutes/'+str(term)+'?market=KRW-'+coin_nm+'&count=2'
headers = {"Accept": "application/json"}
response = requests.request("GET", url, headers=headers)
cur_data = json.loads(response.text)
for i in cur_data:
    print(i)
low_price  = cur_data[1]['low_price']
high_price = cur_data[1]['high_price']
end_price = cur_data[1]['trade_price']
gap = high_price - low_price
time = cur_data[1]['candle_date_time_kst']

# 진입가격 계산
cur_time = cur_data[0]['candle_date_time_kst']
cur_price = cur_data[0]['trade_price']
in_price = end_price + gap*K
print(f'term : {term} min')
print(f'time : {time}')
print(f'high_price : {format(int(high_price), ",")}')
print(f'low_price  : {format(int(low_price), ",")}')
print(f'end_price  : {format(int(end_price), ",")}')
print(f'gap        : {format(int(gap), ",")}')
print(f'cur_time   : {cur_time}')
print(f'cur_price  : {format(int(cur_price), ",")}')
print(f'in_price   : {format(int(in_price), ",")}')
