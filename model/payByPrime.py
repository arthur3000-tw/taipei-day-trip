import os
import json
import urllib.request
import datetime
from model.OrderModel import OrderInput
from model.TapPayPrimeModel import PrimeOutput


def payByPrime(orderInput: OrderInput):
    # 取得 url, headers, body
    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.environ.get("PARTNER_KEY"),
    }
    data = json.dumps({
        "prime": orderInput.prime,
        "partner_key": os.environ.get("PARTNER_KEY"),
        "merchant_id": "arthur3000_ESUN",
        "details": "TapPay Test",
        "amount": orderInput.order.price,
        "cardholder": {
            "phone_number": orderInput.order.contact.phone,
            "name": orderInput.order.contact.name,
            "email": orderInput.order.contact.email,
        },
    }).encode()
    # 產生 request 物件
    request = urllib.request.Request(url=url, headers=headers, data=data)
    # 送出 request
    with urllib.request.urlopen(request) as response:
        response_body = json.loads(response.read().decode("utf-8"))
    # 取得 response
    status = response_body["status"]
    message = response_body["msg"]
    rec_trade_id = response_body["rec_trade_id"]
    transaction_time = datetime.datetime.fromtimestamp(response_body["transaction_time_millis"]/1000)
    # 回傳結果
    return PrimeOutput(status=status,message=message,rec_trade_id=rec_trade_id,transaction_time=transaction_time)