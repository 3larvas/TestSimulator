import requests
import json
import csv
from datetime import datetime, timedelta
import time

term = 5
coin_nm = 'BTC'
test_term = 90 # days
cur_date = datetime.now().date()
end_date = cur_date - timedelta(days=test_term)
idx_date = cur_date - timedelta(days=1)
print(f'start_date : {idx_date}')

f = open('data/'+coin_nm+'_data.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

while(idx_date.strftime('%Y%m%d') >= end_date.strftime('%Y%m%d')):
    print(idx_date.strftime('%Y-%m-%d %H:%M:%S'))
    url = 'https://api.upbit.com/v1/candles/minutes/'+str(term)+'?market=KRW-'+coin_nm+'&to='+idx_date.strftime('%Y-%m-%d %H:%M:%S')+'&count=200'
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    cur_data = json.loads(response.text)
    time.sleep(0.5)
    for data in cur_data:
        wr.writerow([data])
    idx_date = datetime.strptime(cur_data[-1]['candle_date_time_utc'], '%Y-%m-%dT%H:%M:%S')
    print(f'end date : {idx_date}')

f.close()

