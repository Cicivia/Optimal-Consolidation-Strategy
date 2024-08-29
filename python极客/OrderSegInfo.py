class OrderSeInfo(object):  # 订单分段(segment)信息对象
    order_code = None  # 订单编号
    orderStart = None  # 起始城市
    orderEnd = None # 目的城市
    seNum = None  # 段号
    route_code = None  # 分段线路编号
    seStart = None  # 分段起始城市
    seEnd = None  # 分段目的城市
    carNum = None  # 车辆编号
    d = None# 距离

    def __init__(self, order, seNum, route_code, seStart, seEnd, carNum, d):  # 初始化订单分段(segment)信息
        self.order_code = order.order_code  # 订单编号
        self.orderStart = order.start  # 起始城市
        self.orderEnd = order.end  # 目的城市
        self.seNum = seNum  # 段号
        self.route_code = route_code  # 分段线路编号
        self.seStart = seStart  # 分段起始城市
        self.seEnd = seEnd  # 分段目的城市
        self.carNum = carNum  # 车辆编号
        self.d = d  # 距离

    def show(self):
        print(self.order_code,
              self.orderStart,
              self.orderEnd,
              self.seNum,
              self.route_code,
              self.seStart,
              self.seEnd,
              self.carNum,
              self.d)


