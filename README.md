# 极客竞赛

## 运行环境

*   Python 3.9 或更高版本
*   openpyxl 3.0.7 或更高版本
*   pandas 1.2.4 或更高版本

## 部署步骤

1.  下载并安装 Python 3.9 及以上版本，详见官方文档 <https://www.python.org/downloads/>
2.  打开命令行界面，使用以下命令安装所需的第三方模块：
    pip install openpyxl pandas

## 启动应用程序

1.  下载并解压应用程序代码。
2.  在命令行界面中，导航到应用程序代码的目录下。
3.  使用以下命令启动应用程序：
    python main.py

## 入参出参说明

该程序的入口无需输入参数，而需把“集货策略赛题数据.xlsx”置于与程序文件所在目录下，与程序文件保持同级。

## 项目程序文件

### 项目下的python程序文件有：

*   main.py：项目程序的运行入口，无需参数

*   loadms.g.py: 项目函数库，自定义函数均存放于此

*   Order.py：订单对象

*   Truck.py：卡车对象

*   OrderSegInfo.py：订单分段信息存储对象

*   change.py：修改原订单顺序

*   Collection\_point.py：寻找集货点顺序

*   dijkstra.py：寻找最短路径

*   sort.xlsl: 修改订单顺序后的订单文件

*   结果.xlsx：excel表格文件，在程序运行前已在第一行设置好列名:订单号、起始城市、目的城市、段号、分段路线编号、分段起始城市、分段目的城市、车辆编号、距离。

*   集货策略赛题数据.xlsx：根据主办方要求删去无效可用路段信息和无效订单信息后保存的文件

### loadmsg.py函数库说明：

*   load(msg) # 该函数根据输入参数msg不同加载不同赛题数据，以DateFrame形式返回

*   getAllCity(route\_msg)  # 该函数以列表的形式返回所有城市信息 参数为dataframe类型的线路数据

*   last\_index(lst, element)  # 返回列表lst中element元素最后依次出现的下标

*   getCTOther(route\_msg) #（起始城市索引表）该函数返回一个字典，键值分别是城市名和该城市在route\_msg中对应的row范围，例：'上海': \[5，342]（起始城市为上海的路线在路线表中5到342列）

*   getroute(path, end)  # 根据迪杰斯特拉算法的path数组和目的城市找到返回最短路径上的所有节点

*   trucksisavali(trucks)  # 参数为车队列表，查询该车队是否有位置配货

*   expand\_num\_C(num)  # 将整型变量转换为6位的字符串，并在左边用“0”补齐

*   updatabyroute(route, route\_msg, STABLE\_route\_msg, order, ctother, CARNUM)  # 根据rouet更新路线权重

