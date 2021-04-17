import AlgoPlus as ap


@ap.ap_marketdata_callback_wraps
def on_marketdata_event(data):
    print(data)


@ap.ap_order_callback_wraps
def on_order_event(event_id, order, position, cash):
    print("on_order", order)


def on_event(event_id, field, islast, error_id, error_msg):
    field = ap.decode_ctp_event_field(event_id, field)
    if islast:
        print("event", event_id, field)


def on_loop():
    global counter
    global trader
    global standard_list

    counter += 1
    print("loop", counter)
    if counter == 1:
        ap.cancelOrderAll(trader)
    elif counter == 100:
        for item in standard_list:
            ap.buy(trader, item, 1, ap.ENUM_OrderType_FrontierLimitAndWait, 0)


if __name__ == '__main__':

    login = ap.CAPLoginField()

 	# 关于授权的说明：http://algo.plus/algoplus/0106001.html
	# 加QQ号2565657639(注明AlgoPlus授权)，或者公众号AlgoPlus后台留言，申请模拟交易授权。    login.License = ""
    login.UserType = ap.ENUM_UserType_NSIGHTFuture
    login.UserID = ""
    login.InvestorID = ""
    login.Password = ""
    login.TraderFront = "tcp://210.14.72.12:4600"
    login.MdFront = "tcp://210.14.72.12:4602"
    login.ConnectTimeout = 0
    login.TaskExecuteGap = ap.MICROSECONDS_IN_SECOND * 2
    login.BasePath = "./"
    login.BrokerID = "10010"
    login.AppID = "0"
    login.AuthCode = "0"

    counter = 0
    standard_list = ["bc2106", "bu2106", "cu2105", "fu2105", "i2109", "j2105", "jm2105"]
    trader = ap.init(0, login, on_marketdata_event, on_order_event, on_event, on_loop)
    if trader is not None:
        ap.subscribe(trader, standard_list)
        ap.loop()
    else:
        init_error_id = ap.getInitError()
        print(init_error_id)
