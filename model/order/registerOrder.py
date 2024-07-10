from fastapi.responses import JSONResponse
from model.tappay.payByPrime import payByPrime
from model.order.generateOrderNumber import generateOrderNumber
from model.booking.orderBooking import orderBooking
from model.order.OrderModel import OrderInput, OrderOutput, OrderInfo, Payment
from model.user.UserModel import UserInfo
from model.ResponseModel import Error

def registerOrder(myDB, orderInput: OrderInput, userInfo: UserInfo):
    # TapPay order
    primeOutput = payByPrime(orderInput)
    if primeOutput.status != 0:
        return JSONResponse(status_code=400, content=Error(error=True, message="付款失敗").model_dump())
    # Generate order number
    orderNumber = generateOrderNumber(primeOutput)
    # Get booking id and change status
    status = orderBooking(myDB,userInfo,orderInput)
    if status.status_code == 1:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤，未找到此訂單(1)").model_dump())
    elif status.status_code == 2:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤，未找到此訂單(2)").model_dump())
    elif status.status_code == 3:
        pass
    # 資料庫
    sql = "INSERT INTO orders (booking_id,status,message,trade_id,transaction_time,order_number,contact_name,contact_email,contact_phone) \
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (status.data,primeOutput.status,primeOutput.message,primeOutput.rec_trade_id,primeOutput.transaction_time,orderNumber,
           orderInput.order.contact.name,orderInput.order.contact.email,orderInput.order.contact.phone)
    result = myDB.insert(sql,val)
    if result == 1:
        return OrderOutput(data=OrderInfo(number=orderNumber,payment=Payment(status=primeOutput.status,message=primeOutput.message)))
    else:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())