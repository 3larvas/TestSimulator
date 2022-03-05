import datetime
import json
import requests
coin_nm = 'ETH'
target_per_1 = 0.3
target_per_2 = 0.5
out_per_1 = target_per_1 * -1
out_per_2 = target_per_2 * -1
out_per_last = out_per_2 * 2
trade_fee = 0.05 / 100
trade_resv_fee = 0.139 / 100
in_price = 3440000

target_price_1 = int(in_price*(target_per_1/100 + (1+trade_fee))/(1-trade_fee))
target_price_2 = int(in_price*(target_per_2/100 + (1+trade_fee))/(1-trade_fee))
out_price_1 = int(in_price*(out_per_1/100 + (1+trade_fee))/(1-trade_fee))
out_price_2 = int(in_price*(out_per_2/100 + (1+trade_fee))/(1-trade_fee))
out_price_last = int(in_price*(out_per_last/100 + (1+trade_fee))/(1-trade_resv_fee))

def cal_target():
    url = 'https://api.upbit.com/v1/candles/minutes/5?market=KRW-'+coin_nm+'&count=1'
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    cur_data = json.loads(response.text)
    #------------- print data -------------#
    cur_price = int(cur_data[0].get('trade_price'))
    cur_per = round((cur_price*(1-trade_fee)-in_price*(1+trade_fee))/in_price*100, 2)
    print(f'=============== {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ===============')
    print(f'in_price        : {format(in_price, ",")}')
    print(f'cur_price       : {format(cur_price, ",")}')
    print(f'cur_per         : {cur_per} %')
    print('-------- target  --------')
    print(f'target_1({target_per_1} %) : {format(target_price_1, ",")}')
    print(f'target_2({target_per_2} %) : {format(target_price_2, ",")}')
    print('--------   out   --------')
    print(f'out_1({out_per_1} %)   : {format(out_price_1, ",")}')
    print(f'out_2({out_per_2} %)   : {format(out_price_2, ",")}')
    print(f'out_last({out_per_last} %): {format(out_price_last, ",")}')








