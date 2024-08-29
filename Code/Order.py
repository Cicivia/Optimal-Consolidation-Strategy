class Order(object):
    order_code = None  # 订单编号
    start = None
    end = None
    shipInfo = None

    def __init__(self, order_code, start, end):  # 为该订单分配唯一订单编号
        self.order_code = order_code
        self.start = start
        self.end = end
        self.shipInfo = []

    def show(self):
        print(self.order_code, self.start, self.end)
