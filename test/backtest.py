import json
import csv
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

term = 6
coin_nm = 'BTC'
money = 1000000

f = open('data/'+coin_nm+'_data.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
data_list = []
for line in rdr:
    tmp = json.loads(str(line[0]).replace("'", "\""))
    data_list.insert(0,tmp)
f.close()

x_values, y_trade, y_max, y_min, x_highlight, y_highlight, x_money, y_money, y_money_stack = [], [], [], [], [], [], [], [], []

idx, result = 0, 0
total_size = len(data_list)
start_price = data_list[0]['trade_price']
x_money.append(datetime.strptime(data_list[0]['candle_date_time_utc'], '%Y-%m-%dT%H:%M:%S'))
y_money.append(0)
y_money_stack.append(0)
x_highlight.append(datetime.strptime(data_list[0]['candle_date_time_utc'], '%Y-%m-%dT%H:%M:%S'))
y_highlight.append(data_list[0]['trade_price'])

for data in data_list:
    idx += 1
    x_values.append(datetime.strptime(data['candle_date_time_utc'], '%Y-%m-%dT%H:%M:%S'))
    y_trade.append(int(data['trade_price']))
    y_max.append(int(data['high_price']))
    y_min.append(int(data['low_price']))
    # y_money.append(y_money[idx-1])
    if idx > term and idx < total_size - term:
        max_val = max(y_max[idx-term:idx])
        min_val = min(y_min[idx-term:idx])
        gap = max_val - min_val
        in_price = data['opening_price'] + gap * 0.7
        cur_price = data['trade_price']
        cur_date = datetime.strptime(data['candle_date_time_utc'], '%Y-%m-%dT%H:%M:%S')
        if in_price*0.999 < cur_price and cur_price < in_price*1.001:
            x_highlight.append(cur_date)
            y_highlight.append(cur_price)
            sell_time = datetime.strptime(data_list[idx + term]['candle_date_time_utc'], '%Y-%m-%dT%H:%M:%S')
            sell_price = data_list[idx+term]['trade_price']
            earn_money = (sell_price-cur_price)*0.999
            result += earn_money
            x_money.append(cur_date)
            y_money.append(earn_money)
            y_money_stack.append(y_money_stack[-1] + earn_money)
            print(f'date : {cur_date}, cur_price : {cur_price}, sell_price : {sell_price}, earn_money : {sell_price-cur_price}, result : {result}')


percent = round(result/start_price*100,2)
print(f'nun_sel : {len(y_highlight)}')
print(f'percent : {percent} %')
print(f'input : {format(money,",")}, earn : {format(money*(1+percent/100),",")}')

plt.figure(figsize=(16,8))
plt.subplot(3, 1, 1)
plt.plot(x_values, y_trade)
plt.scatter(x_highlight, y_highlight, marker='o', color= 'red')
plt.subplot(3, 1, 2)
plt.plot(x_money, y_money)
plt.scatter(x_highlight, y_money, marker='o', color= 'red')
plt.subplot(3, 1, 3)
plt.plot(x_money, y_money_stack)
plt.tight_layout()
plt.show()
plt.savefig('test.png')
