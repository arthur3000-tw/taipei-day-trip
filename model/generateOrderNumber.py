import datetime
from model.TapPayPrimeModel import PrimeOutput

# 產生訂單號碼
def generateOrderNumber(primeOutput:PrimeOutput):
    today = datetime.datetime.now().strftime("%Y%m%d")
    string = primeOutput.rec_trade_id
    number = ""
    for ch in string[:8:-1]:
        number += str(ord(ch))
    number = today + number
    return number