import pyupbit
import time, datetime
import json
import telegram
import asyncio

# config.json 파일처리 ----------------
with open('config.json','r') as f:
    config = json.load(f)
access = config['UPBIT']['ACCESS-KEY']
secret = config['UPBIT']['SECRET-KEY']
# ------------------------------------

upbit = pyupbit.Upbit(access, secret)

# print(upbit.get_balance("KRW-BTC"))
# print(upbit.get_balance("KRW"))
print(upbit.get_balances())

def comma3(num):    # 숫자 3자리마다 ,(comma) 찍는 함수
    value = str(int(float(str(num))))
    reversed_value = value[::-1]
    formatted_value = ",".join([reversed_value[i:i+3] for i in range(0, len(reversed_value), 3)])
    formatted_value = formatted_value[::-1]
    # print(formatted_value)
    return(formatted_value)

output = f"BTC 시세: {comma3(int(float(str(pyupbit.get_current_price('KRW-BTC')))))}"
# print(f"BTC 시세: {comma3(int(float(str(pyupbit.get_current_price('KRW-BTC')))))}")
data = upbit.get_balances() # 잔고 전체가 dictionay 로 반환됨

krw = 0

for item in data:
    cur = item['currency']
    bal = item['balance']
    avg = item['avg_buy_price']
    
    if cur == "KRW":
        output = output + f"\n{cur} 잔고: {comma3(int(float(str(bal))))}"
        # print(f"{cur} 잔고: {comma3(int(float(str(bal))))}")
        krw = krw + float(bal)
    else:   # BTC
        # print(pyupbit.get_current_price("KRW-BTC"))
        current_btc = pyupbit.get_current_price("KRW-BTC")
        bal_krw = current_btc * float(bal)  # 계좌잔고 (bal * 현재가)
        # print(bal_krw)
        output = output + f"\n{cur} 잔고: {bal},\n 평단: {comma3(int(float(str(avg))))},\n 총평가금액: {comma3(int(float(str(bal_krw))))}"
        # print(f"{cur} 잔고: {bal}, 평단: {comma3(int(float(str(avg))))}, 총평가금액: {comma3(int(float(str(bal_krw))))}")
        krw = krw + bal_krw

# print(f"총잔고: {int(float(str(krw)))}")
output = output + f"\n총잔고: {comma3(krw)}"
# print(f"총잔고: {comma3(krw)}")

print(output)
msg_content = output

# telegram 메세지 발송
async def tele_push(content): #텔레그램 발송용 함수
    # config.json 파일처리 ----------------
    with open('config.json','r') as f:
        config = json.load(f)
    token = config['TELEGRAM']['TOKEN']
    chat_id = config['TELEGRAM']['CHAT-ID']
    # ------------------------------------
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    bot = telegram.Bot(token = token)
    await bot.send_message(chat_id, formatted_time + "\n" + content)

# asyncio.run(tele_push(msg_content)) #텔레그램 발송 (asyncio를 이용해야 함)%
