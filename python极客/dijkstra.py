import pandas as pd
# from Collection_point import collection_points
def dijkstra(graph, start, end):
    """
    使用Dijkstra算法获取两个城市之间的最短路径和距离
    graph：图
    start：起始城市
    end：结束城市
    """
    # 初始化距离和前置节点
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0
    previous_vertices = {vertex: None for vertex in graph}
    # 用来存储未处理的节点
    vertices = set(graph.keys())
    while vertices:
        # 在未处理的节点中找到距离最小的节点
        current_vertex = min(vertices, key=lambda vertex: distances[vertex])
        # 如果距离为无限大，则无法到达
        if distances[current_vertex] == float('inf'):
            break
        # 处理当前节点的邻居
        for neighbor, weight in graph[current_vertex].items():
            alternative_route = distances[current_vertex] + weight
            if alternative_route < distances[neighbor]:
                distances[neighbor] = alternative_route
                previous_vertices[neighbor] = current_vertex
        # 将当前节点标记为已处理
        vertices.remove(current_vertex)
    # 构建最短路径
    path, current_vertex = [], end
    while previous_vertices[current_vertex] is not None:
        path.insert(0, current_vertex)
        current_vertex = previous_vertices[current_vertex]
    if path:
        path.insert(0, current_vertex)
    # 返回最短路径和距离
    return distances[end]
# 读取数据
routes = pd.read_excel('集货策略赛题数据.xlsx', sheet_name='赛题数据-可用路线')
# 构建图
graph = {}
for _, row in routes.iterrows():
    start, end, distance,number = row['起始地'], row['目的地'], row['距离'],row['线路编号']
    if start not in graph:
        graph[start] = {}
    if end not in graph:
        graph[end] = {}
    graph[start][end] = distance
    graph[end][start] = distance
# 输入起始地和目的地
start_city = input('三明市')
end_city=input('天津市')
d=dijkstra(graph,start_city,end_city)
print(d)
# s,p=[],[]
# for end_city in collection_points:
#     # 计算最短路径和距离
#     if end_city==start_city:
#         continue
#     path, distance = dijkstra(graph, start_city, end_city)
#     p.append(path)
#     s.append(distance)
#     # 输出结果
#     if path:
#         print('最短路径：', ' -> '.join(path))
#         print('距离：', distance)
#     else:
#         print('无法到达目的地。')
# #最小距离
# def min_distance(start_city,end_city):
#     path, distance = dijkstra(graph, start_city, end_city)
#     return distance
# #寻找到所有集货点距离的最小地区
# def min_collection_distance(start_city,end_city):
#     try:
#         s, p = [], []
#         for collect_city in collection_points:
#             # 计算最短路径和距离
#             if collect_city == start_city:
#                 continue
#             elif min_distance(collect_city,end_city)>=min_distance(start_city,end_city):
#                 continue
#             # elif min_distance(start_city,collect_city)>500:
#             #     continue
#             path, distance = dijkstra(graph, start_city, collect_city)
#             p.append(path)
#             s.append(distance)
#         min_dis=p[s.index(min(s))][-1]
#         return min_dis
#     except:
#         # 出现异常时执行的代码
#         return -1
#
# def get_route_number(start_city, end_city):
#     # 读取路线数据
#     routes = pd.read_excel(r'C:\Users\z1015\Desktop\集货策略赛题数据.xlsx', sheet_name='赛题数据-可用路线')
#     # 构建图
#     graph = {}
#     for _, row in routes.iterrows():
#         start, end,  number = row['起始地'], row['目的地'], row['线路编号']
#         if start not in graph:
#             graph[start] = {}
#         if end not in graph:
#             graph[end] = {}
#         graph[start][end] = number
#         graph[end][start] = number
#     # 输出结果
#     if start_city not in graph or end_city not in graph:
#         return None
#     route_number = graph[start_city].get(end_city)
#     return route_number
