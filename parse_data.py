#coding:utf8
import csv
from pprint import pprint

class Order:
    def __init__(self, id, tix_count, tix_type, order_time, pay_time):
        self.id = id
        self.tix_count = tix_count
        self.tix_type = tix_type
        self.order_time = order_time
        self.pay_time = pay_time

        pass

    def __lt__(self, other):
        return self.order_time < other.order_time

    def __repr__(self):
        return 'id:{},tix_count:{}'.format(self.id, self.tix_count)


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


    # 将order用编号代替
    cur_ord_id = 1
    for o in order_info:
        ord = Order(id= '%03d'% cur_ord_id, tix_count=order_tix_count_map[o[4]], order_time=o[2], pay_time=0, tix_type='PS')
        orders.append(ord)
        cur_ord_id += 1

    return orders


def parse_seats_data(path, area):
    """解析csv数据, 获取该区域的数据"""

    area_seats = [] # 保存当前区域的座位CSV原始数据
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for r in reader:
            # 过滤不是该区域的数据
            if r[0] != area: continue
            area_seats.append(r)

    # 获取该区域的行数和列数
    area_rows = 0 # 当前区域的总行数
    area_colunms = 0  # 当前区域总列数
    row_name_index_map = {} # 用于记录行名对应行索引
    if True:
        for s in area_seats:
            if s[1] not in row_name_index_map:
                # 记录行名对应行索引
                row_name_index_map[s[1]] = len(row_name_index_map)

                # 增加行数
                area_rows += 1

            # 获取最大列数
            if int(s[2]) > area_colunms:
                area_colunms = int(s[2])

    # 构造二维数组
    seats_2d_array = []
    for _ in range(area_rows):
        # 这里默认将所有作为设置 'X',
        seats_2d_array.append( ['X'] * area_colunms )

    # 将存在的座位放开, 设置为 'O'
    for s in area_seats:
        row_idx = row_name_index_map[ s[1] ]
        col_idx = int(s[2]) - 1

        # 设置 'O'
        seats_2d_array[row_idx][col_idx] = 'O'

    return seats_2d_array







def main():
    # ol = parse_order_data('./data/order_data.csv')
    # pprint(ol)
    # print('========== {}'.format(len(ol)))

    # area_sorts = ['113', '114', '112', '111', '110', '109']
    array = parse_seats_data('./data/seats.csv', '113')
    for r in range(len(array)):
        output = ''
        for c in range(len(array[0])):
            output += '{}'.format(array[r][c])
            if c != len(array[0]) - 1:
                output += ','
        print(output)
    pass

if __name__ == '__main__':
    main()
