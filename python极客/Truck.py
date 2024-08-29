class Truck(object):  # 卡车
    route_code = None  # 该车所在分段线路编号
    orders = None   # 该车所有订单

    def __init__(self, route_code):  # 为该车分配路线编号
        self.route_code = route_code
        self.orders = []