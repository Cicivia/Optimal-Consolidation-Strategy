import itertools
import loadmsg
import OrderData
from Order import Order
INF = 10000  # 定义无穷大
STABLE_route_msg = loadmsg.load('路线信息')  # 载入路线信息（column['路线编号', '起始城市', '目的城市', '距离', '车辆信息']，全局唯一不变）
route_msg = loadmsg.load('路线信息')  # 载入路线信息(column['路线编号', '起始城市', '目的城市', '距离', '车辆信息']，距离根据车辆安排情况调整)
order_msg = loadmsg.load('订单信息')  # 载入订单信息(column['订单编号', '起始城市', '目的城市'])
ctother = loadmsg.getCTOther(route_msg)  # 城市索引表
orders = []  # 存放所有订单信息，方便订单结果数据录入
for index, row in order_msg.iterrows():  # 为每个订单安排路线
    order = Order(row['订单编号'], row['起始城市'], row['目的城市'])  # 创建该订单对象，配送完此订单后加入orders列表
    print('为订单', row['订单编号'], '安排线路')
    # 下面通过迪杰斯特拉算法找到订单order的最短路径
    cities = loadmsg.getAllCity(route_msg)  # 定义所有城市名称列表（包括起始城市和目的城市）
    dis = dict(itertools.zip_longest(cities, [INF] * len(cities)))  # 定义字典 城市名称：距离起始城市距离
    path = dict(itertools.zip_longest(cities, [-1] * len(cities)))  # 定义字典 城市名称：路径上的上一个城市
    s = []  # 定义集合， 放置已确定最短路径的城市
    # 迪杰斯特拉算法准备工作
    dis[order.start] = 0  # 将起始地再dis字典中的对应元素初始化为0
    # 迪杰斯特拉算法核心
    while order.end not in s:  # 当未确定目的地的最短路径时执行循环体
        # 将距离起始城市最小且未加入s的城市c加入s
        c = None
        if len(s) == len(dis):
            print("所有城市均找到最短路径")
            break
        for key, value in dis.items():  # 找到第一个未加入s的城市
            if key not in s:
                c = key
                break
        for key, value in dis.items():  # 找到距离起始城市最小且未加入s的城市
            if value < dis[c] and key not in s:
                c = key
        s.append(c)
        # 更新城市c邻近的城市距离
        if c in ctother:  # 城市c有目的城市
            i = ctother[c][0]
            j = ctother[c][1]
            while i <= j:
                new_dis = dis[c] + eval(route_msg.loc[i, '距离'])
                if new_dis < dis[route_msg.loc[i, '目的城市']]:  # 新的距离小于当前距离
                    dis[route_msg.loc[i, '目的城市']] = new_dis
                    # 更新目的城市在path中的信息
                    path[route_msg.loc[i, '目的城市']] = c
                i += 1
    route = loadmsg.getroute(path, order.end)  # 获取最短路径上所有结点，以列表存储
    print(route)