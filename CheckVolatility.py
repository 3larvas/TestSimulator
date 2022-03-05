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

def checkVolatility():
    # --------------- collect last data and save at DB --------------- #
    url = 'https://api.upbit.com/v1/candles/minutes/'+str(term)+'?market=KRW-'+coin_nm+'&count=6'
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

    # --------------- Check Volatility --------------- #
    select_sql = f'select * from coin_price_data where unit = \"5m\"  order by `date` desc limit 20'
    cur.execute(select_sql)
    cur_list = cur.fetchall()
    data_list = []
    for data in cur_list:
        tmp = dict()
        tmp['coin_nm'] = data[0]
        tmp['unit'] = data[1]
        tmp['date'] = data[2]
        tmp['open_price'] = data[3]
        tmp['end_price'] = data[4]
        tmp['high_price'] = data[5]
        tmp['low_price'] = data[6]
        tmp['trade_vol'] = data[7]
        tmp['trade_total_price'] = data[8]
        data_list.append(tmp)

    conn.close

    start_price = data_list[0]['open_price']
    cur_price = data_list[0]['end_price']
    max_price = data_list[1]['high_price']
    min_price = data_list[1]['low_price']
    for data in data_list[1:]:
        max_price = max(max_price, data['high_price'])
        min_price = min(min_price, data['low_price'])
    gap = max_price-min_price
    in_price = start_price + gap * 0.5
    msg = f'=============\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \nmax : {format(max_price, ",")}\nmin : {format(min_price, ",")}\ngap : {format(gap, ",")}\nin_price : {format(in_price, ",")}'
    print(msg)
    if in_price*0.999 < cur_price and cur_price < in_price*1.001:
        print(f'------------- 변동성 돌파 감지 -------------')
        response = requests.post("https://slack.com/api/chat.postMessage",
                                 headers={"Authorization": "Bearer " + 'xoxb-3113764770950-3120486752259-NHr6XHlBoakF4VojUO7lFajT'},
                                 data={"channel": '#alarm_system', "text": msg})
        print(response.content)


checkVolatility()