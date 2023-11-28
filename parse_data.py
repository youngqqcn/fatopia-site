#coding:utf8
import csv
from pprint import pprint

from seats import Order


def parse_order_data(path):
    """获取订单数据"""

    orders = []
    order_tix_count_map = {}
    order_info = []

    with open(path, 'r') as file:
        reader = csv.reader(file)

        line = 0
        for row in reader:
            # 不解析首行
            if line == 0:
                line += 1
                continue

            order_id = row[4]
            if order_id not in order_tix_count_map:
                order_tix_count_map[order_id] = 1
                order_info.append( row )
            else:
                order_tix_count_map[order_id] += 1

    for o in order_info:
        ord = Order(id=o[4], tix_count=order_tix_count_map[o[4]], order_time=o[2], pay_time=0)
        orders.append(ord)

    return orders


def parse_seats_data(path):
    """解析座位数据"""

    areas_map = {}

    # 获取不同区域
    with open(path, 'r') as file:
        reader = csv.reader(file)
        line = 0
        for r in reader:
            # 不解析首行
            if line == 0:
                line += 1
                continue

            area = r[0]
            row = r[1]
            column = r[2]
            if area not in areas_map:
                areas_map[ area ] = r[0]
                areas_map[area] = {'row': set([row]), 'column': set([column]) }
            else:
                areas_map[area]['row'].add( row )
                areas_map[area]['column'].add( column )

    return areas_map


def make_2darray(area_sorts, areas_map):
    """
    将同一票型不同区域合并,构建一个2维数组
    根据区域的优先级顺序,依次构建
    列数, 取决于列数最多的区域
    那列数不够的, 用标记符号填充
    """

    total_rows = 0
    max_column = 0
    row_map = {} # 记录不同行对于的区域
    for _, v in areas_map:
        # 行
        total_rows += len(v['row'])
        for i in range(len(v['row'])):

            pass

        # 列
        if len(v['column']) > max_column:
            max_column = len(v['column'])
        if max(v['column']) > max_column:
            # 有些可能不连续, 仍然按照最多列数
            max_column = max(v['column'])

    pass



def main():
    # parse_order_data('./data/order_data.csv')
    am = parse_seats_data('./data/seats.csv')
    pprint(am)
    pass

if __name__ == '__main__':
    main()
