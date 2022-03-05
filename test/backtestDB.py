from matplotlib import pyplot as plt
import mariadb
term = 6
coin_nm = 'KRW-BTC'
money = 1000000
start_date = '2022-01-31'
end_date = '2022-02-17'
conn = mariadb.connect(user="root", password="root123", host="127.0.0.1", port=3306, database="coin_data")
cur = conn.cursor()
select_sql = f'select * from coin_price_data where unit = \"5m\" and coin_nm = \"{coin_nm}\" and date between \"{start_date}\" and \"{end_date}\"'

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

x_values, y_trade, y_max, y_min, x_highlight, y_highlight, x_money, y_money, y_money_stack = [], [], [], [], [], [], [], [], []

idx, result = 0, 0
total_size = len(data_list)
start_price = data_list[0]['end_price']
x_money.append(data_list[0]['date'])
y_money.append(0)
y_money_stack.append(0)
x_highlight.append(data_list[0]['date'])
y_highlight.append(data_list[0]['end_price'])

for data in data_list:
    idx += 1
    x_values.append(data['date'])
    y_trade.append(int(data['end_price']))
    y_max.append(int(data['high_price']))
    y_min.append(int(data['low_price']))
    # y_money.append(y_money[idx-1])
    if idx > term and idx < total_size - term:
        max_val = max(y_max[idx-term:idx])
        min_val = min(y_min[idx-term:idx])
        gap = max_val - min_val
        in_price = data['open_price'] + gap * 0.7
        cur_price = data['end_price']
        cur_date = data['date']
        if in_price*0.999 < cur_price and cur_price < in_price*1.001:
            x_highlight.append(cur_date)
            y_highlight.append(cur_price)
            sell_time = data_list[idx + term]['date']
            sell_price = data_list[idx+term]['end_price']
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
