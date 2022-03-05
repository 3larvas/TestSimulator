import mariadb
import requests
import json
from datetime import datetime, timedelta
import time

conn = mariadb.connect(user="root", password="root123", host="127.0.0.1", port=3306, database="coin_data")
cur = conn.cursor()
insert_sql = 'replace into coin_price_data values'

term = 5
coin_nm = 'BTC'
test_term = 300 # days
cur_date = datetime.now().date()
end_date = cur_date - timedelta(days=test_term)
idx_date = cur_date # - timedelta(days=1)
print(f'start_date : {idx_date}')

while(idx_date.strftime('%Y%m%d') >= end_date.strftime('%Y%m%d')):
    print(f'-------- idx_date : {idx_date.strftime("%Y-%m-%d %H:%M:%S")} --------')
    # for minutes
    url = 'https://api.upbit.com/v1/candles/minutes/'+str(term)+'?market=KRW-'+coin_nm+'&to='+idx_date.strftime('%Y-%m-%d %H:%M:%S')+'&count=200'
    # for day
    # url = "https://api.upbit.com/v1/candles/days?market=KRW-"+coin_nm+'&to='+idx_date.strftime('%Y-%m-%d %H:%M:%S')+"&count=50"

    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    cur_data = json.loads(response.text)
    time.sleep(0.5)
    insert_data = ''
    for data in cur_data:
        insert_data += f'(\"{data["market"]}\", \"{term}m\", \"{datetime.strptime(data["candle_date_time_utc"], "%Y-%m-%dT%H:%M:%S")}\", ' \
               f'{data["opening_price"]}, {data["trade_price"]}, {data["high_price"]}, {data["low_price"]},' \
               f' {data["candle_acc_trade_volume"]}, {data["candle_acc_trade_price"]}, \"{datetime.now()}\"),'
    sql_str = insert_sql + insert_data[:-1] + ';'
    print(sql_str)
    cur.execute(sql_str)
    conn.commit()

    idx_date = datetime.strptime(cur_data[-1]['candle_date_time_utc'], '%Y-%m-%dT%H:%M:%S')
    print(f'end date : {idx_date}')


conn.close()