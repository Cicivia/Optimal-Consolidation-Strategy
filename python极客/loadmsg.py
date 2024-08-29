import openpyxl
import pandas as pd
from OrderSegInfo import OrderSeInfo
from Truck import Truck


def load(msg):  # 该函数根据输入参数msg不同加载不同赛题数据，以DateFrame形式返回
    excel = openpyxl.load_workbook('集货策略赛题数据.xlsx')  #打开赛题数据文件
    if msg == '路线信息':
        sheet1 = excel['赛题数据-可用路线']  # 获取路线信息表格
        route_code = []  # 路线编号
        s = []  # 起始地
        e = []  # 目的地
        d = []  # 距离
        car = []  # 该线路车辆情况
        i = 2
        while sheet1['A' + str(i)].value is not None:
            route_code.append(sheet1['A' + str(i)].value)
            s.append(sheet1['B' + str(i)].value)
            e.append(sheet1['C' + str(i)].value)
            d.append(sheet1['D' + str(i)].value)
            car.append([])
            i += 1
        df = pd.DataFrame({'路线编号': route_code, '起始城市': s, '目的城市': e, '距离': d, '车辆信息': car})
        return df
    elif msg == '订单信息':
        sheet1 = excel['赛题数据-订单']
        order_code = []  # 订单编号
        s = []  # 起始城市
        e = []  # 目的城市
        i = 2
        while sheet1['A' + str(i)].value is not None:
            order_code.append(sheet1['A' + str(i)].value)
            s.append(sheet1['B' + str(i)].value)
            e.append(sheet1['C' + str(i)].value)
            i += 1
        df = pd.DataFrame({'订单编号': order_code, '起始城市': s, '目的城市': e})
        return df


def getAllCity(route_msg):  # 该函数以列表的形式返回所有城市信息 参数为dataframe类型的线路数据
    point = []
    for index, row in route_msg.iterrows():
        point.append(row['起始城市'])
        point.append(row['目的城市'])
    return list(set(point))


def last_index(lst, element):  # 返回列表lst中element元素最后依次出现的下标
    indexes = [i for i in range(len(lst)) if lst[i] == element]
    return indexes[-1] if indexes else None


def getCTOther(route_msg):  # （起始城市索引表）该函数返回一个字典，键值分别是城市名和该城市在route_msg中对应的row范围，例：'上海': [5，342]（起始城市为上海的路线在路线表中5到342列）
    allcity = []  # 记录所有路线的起始城市， 包括重复
    city = []  # 记录所有路线的起始城市， 不重复
    for index, row in route_msg.iterrows():  # 构造完成上面两个列表
        allcity.append(row['起始城市'])
        if row['起始城市'] not in city:
            city.append(row['起始城市'])
    ctother = dict.fromkeys(city)  # 创建一个字典，以所有城市唯一名称为键，值暂时为空
    for key in ctother.keys():  # 为每一个键赋值（寻找每个起始城市在路线表中的范围）
        ctother[key] = []
        start = allcity.index(key)  # 第一次出现的位置
        ctother[key].append(start)
        end = last_index(allcity, key)  # 最后一次出现的位置
        ctother[key].append(end)
    return ctother


def getroute(path, end):  # 根据迪杰斯特拉算法的path数组和目的城市找到返回最短路径上的所有节点
    k = None
    for key, value in path.items():
        if key == end:
            k = key
            break
    route = [k]
    while path[k] != -1:
        route.insert(0, path[k])
        k = path[k]
    return route


def trucksisavali(trucks):  # 参数为车队列表，查询该车队是否有位置配货
    if not trucks:  # 没有车辆
        return False
    else:  # 有车辆
        if len(trucks[len(trucks)-1].orders) < 20:  # 最后一辆车有空位
            return True
        else:  # 所有车都没有空位
            return False


def expand_num_C(num):
    exp_num = str(num).zfill(4)  # 将整型变量转换为6位的字符串，并在左边用“0”补齐
    return 'C' + exp_num


def updatabyroute(route, route_msg, STABLE_route_msg, order, ctother, CARNUM):
    seNum = 1  #段号从1开始计算
    for num in range(0, len(route) - 1):  # 遍历路线上的所有路段
        start, end = ctother[route[num]][0], ctother[route[num]][1]

        row = None  # 找到对应地址段在路线信息中的位置（行索引），赋值给row
        while start <= end:
            if route_msg.loc[start, '目的城市'] == route[num + 1]:
                row = start
                break
            start += 1

        print('处理线路', route_msg.loc[row, '起始城市'], '-', route_msg.loc[row, '目的城市'])

        if not trucksisavali(route_msg.loc[row, '车辆信息']):  # 没有空位则增派车辆
            new_truck = Truck(expand_num_C(CARNUM[0]))  # 给车辆分配编号
            CARNUM[0] += 1
            route_msg.loc[row, '车辆信息'].append(new_truck)
            print('为线路', route_msg.loc[row, '起始城市'], '-', route_msg.loc[row, '目的城市'], "增加车辆")

        route_msg.loc[row, '车辆信息'][len(route_msg.loc[row, '车辆信息']) - 1].orders.append(order)  # 把订单装入最后一辆车
        carNum = route_msg.loc[row, '车辆信息'][len(route_msg.loc[row, '车辆信息']) - 1].route_code
        order.shipInfo.append(OrderSeInfo(order, seNum, route_msg.loc[row, '路线编号'], route_msg.loc[row, '起始城市'], route_msg.loc[row, '目的城市'], carNum, STABLE_route_msg.loc[row, '距离']))
        seNum += 1;

        print(order.order_code, '装入', route_msg.loc[row, '车辆信息'][len(route_msg.loc[row, '车辆信息']) - 1].route_code)
        if trucksisavali(route_msg.loc[row, '车辆信息']):  # 当前线路仍有空位则置该线路距离权重为0
            route_msg.loc[row, '距离'] = '0'
            print(route_msg.loc[row, '起始城市'], '-', route_msg.loc[row, '目的城市'], '距离权重置为0')
        else:  # 没有空位则置为原值
            route_msg.loc[row, '距离'] = STABLE_route_msg.loc[row, '距离']







