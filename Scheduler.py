import schedule
import time
import CheckDown

schedule.every(5).seconds.do(CheckDown.CheckDown)

while True:
    schedule.run_pending()
    # 5분에 한번씩 BTC 가격 조회, 변동성 돌파 체크
    # 변동성 돌파 시 msg 전송
    time.sleep(180)