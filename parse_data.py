#coding:utf-8
#author: yqq
#date: 2023-11-30
#desc: 解析数据

import csv
import copy
from datetime import datetime
import os

class Order:

    # 订单分组间隔时间(s)
    ORDER_GROUP_GAP_SECONDS = 1

    def __init__(self, id, raw_order_id, tix_count, tix_type, order_time, pay_time, seat_ids  ):
        self.id = str(id)
        self.raw_order_id = str(raw_order_id)
        self.tix_count = int(tix_count)
        self.tix_type = str(tix_type)
        self.order_time = int(order_time)
        self.pay_time = int(pay_time)
        self.seat_ids = list(seat_ids)

        pass

    def __lt__(self, other):
        """对订单排序"""

        # 如果时间间隔非常小,则再按照订单的票数排序, 这样有助于后续贪心算法
        # gas_seconds = 17
        if  abs( self.order_time - other.order_time ) <= self.ORDER_GROUP_GAP_SECONDS:
            return self.tix_count > other.tix_count
        return self.order_time < other.order_time

    def __repr__(self):
        return 'id:{},tix_count:{}'.format(self.id, self.tix_count)




class Seat:
    def __init__(self, id, seat_id, area, row, col):
        self.id = id
        self.seat_id = seat_id
        self.area = area
        self.row = row
        self.col = col

    def __repr__(self) :
        return 'seat_id:{}, {}-{}-{}'.format(self.seat_id, self.area, self.row, self.col)


def parse_order_data(path):
    """获取订单数据"""

    print('ORDER_GROUP_GAP_SECONDS is {}'.format(Order.ORDER_GROUP_GAP_SECONDS))

    orders = []
    order_tix_count_map = {}
    order_info = []
    order_seatids_map = {}   # 订单id 和 座位id 映射


    all_seat_id_set = set()  # 座位id不能重复,  但是，订单ID可以重复

    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        line = 0
        for row in reader:
            # 不解析首行
            if line == 0:
                line += 1
                continue

            seat_id = row[0]
            if seat_id in all_seat_id_set:
                raise Exception('座位订单文件的 座位ID:{}重复!请检查'.format(seat_id))

            all_seat_id_set.add(seat_id)

            order_id = row[6]
            if order_id not in order_tix_count_map:
                order_tix_count_map[order_id] = 1
                order_info.append( row )

                # 座位id
                order_seatids_map[order_id] = [ seat_id]
            else:
                order_tix_count_map[order_id] += 1
                order_seatids_map[order_id].append(seat_id )

    # 将order用编号代替
    cur_ord_id = 1
    for o in order_info:
        order_id = o[6]

        # 解析时间为时间戳
        time_str = o[1]
        ord_ts = datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S')
        ord_ts = int(ord_ts.timestamp())

        ord = Order(id= '%03d'% cur_ord_id,
                    raw_order_id = order_id,
                    tix_count=order_tix_count_map[order_id],
                    order_time=ord_ts,
                    pay_time=0,
                    tix_type='PS',
                    seat_ids= order_seatids_map[order_id]
                    )
        orders.append(ord)
        cur_ord_id += 1

    
    return orders


def parse_seats_data(path, area, special_row_sorts_map):
    """解析csv数据, 获取该区域的数据"""

    area_seats = [] # 保存当前区域的座位CSV原始数据
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        first_line = True
        for r in reader:

            # 第1行是头，跳过
            if first_line :
                first_line = False
                continue

            # 如果不设置区域名，读=第一个区域， 用于测试解析文件,是否正常
            if area == '': area = r[0]

            # 过滤不是该区域的数据
            if r[0] != area: continue
            area_seats.append(r)

    # 所有座位, 防止重复
    all_seat_name_set = set()

    # 获取该区域的行数和列数
    area_rows_counter = 0 # 当前区域的总行数
    area_colunms_max = 0  # 当前区域总列数, 获取最大的列编号，作为列
    row_name_index_map = {} # 用于记录行名对应行索引

    if True:
        # TODO: 目前的优先级只细化到 行(排)级别, 如果有特殊情况需要精确到列级别可以，再说
        # 如果该区域没有设置 行的特殊排序，则按照字母(有些是数字)顺序排序, 因此需要获取所有行名(字母或数字)
        if area not in special_row_sorts_map:
            row_sorts = set()
            for s in area_seats:
                row_name = s[1]
                row_sorts.add(row_name)
                pass
            # 不管是字母还是数字， 按默认升序排序,
            row_sorts = sorted(row_sorts )
            special_row_sorts_map[ area ] = row_sorts

        for s in area_seats:
            row_name = s[1]

            if row_name not in row_name_index_map:
                # 记录行名对应行索引
                row_name_index_map[row_name] = special_row_sorts_map[area].index( row_name )

                # 增加行数
                area_rows_counter += 1

            # 获取最大列数
            col_name = s[2]
            if int(col_name) > area_colunms_max:
                area_colunms_max = int(col_name)

            # 保存当前座位编号，防止重复
            cur_seat_full_name = '{}-{}-{}'.format(area, row_name, col_name )
            if cur_seat_full_name in all_seat_name_set:
                raise Exception("座位文件，座位{}重复".format(cur_seat_full_name))
            all_seat_name_set.add( cur_seat_full_name)

    # 构造二维数组
    seats_2d_array = []
    for _ in range(area_rows_counter):
        # 这里默认将所有作为设置 'X',
        seats_2d_array.append( ['X'] * area_colunms_max )

    # 将存在的座位放开, 设置为 'O'
    for s in area_seats:
        row_idx = row_name_index_map[ s[1] ]
        col_idx = int(s[2]) - 1

        # 设置 'O'
        seats_2d_array[row_idx][col_idx] = 'O'

    # 将key:value 换成 value:key
    row_index_name_map = dict(zip(row_name_index_map.values(), row_name_index_map.keys()))
    return seats_2d_array, row_index_name_map


def convert_solution_to_csv(area, seats, orders, row_index_name_map):

    # 将orders转为 以order.id 为key的dict
    orders_map = { ord.id :  ord for ord in orders   }

    ret = {}
    for row in range(len(seats)):
        for col in range(len(seats[row])):

            # 获取 座位ID
            id = seats[row][col]
            if id == 'X' : continue

            seat_id = -1
            o = orders_map[id]
            seat_id = o.seat_ids.pop(0)

            # 更新
            orders_map[id] = o

            # line = '{},{},{},{},{}\n'.format(id, seat_id, area, row_index_name_map[row], col)
            # print(line.strip())
            # outfile.write(line)
            ret[ seat_id ] = Seat(id=id, seat_id=seat_id, area= area,row= row_index_name_map[row],col=col )
    return ret



def output_csv_result(order_csv_path, output_csv_path, csv_data):

    if not os.path.exists(order_csv_path):
        print('文件不存在:{}'.format(order_csv_path))
        return

    output_seats = [] # 保存当前区域的座位CSV原始数据
    header = ''
    with open(order_csv_path, 'r', encoding='utf-8') as infile:

        lines = []
        raw_lines = infile.readlines()
        header = raw_lines[0].strip()
        for l in raw_lines[1:]:
            l = l.strip()
            lines.append(l.split(','))

        for x in lines:
            seat_id = x[0]
            if seat_id in csv_data:
                s = csv_data[seat_id] # 已排座位信息

                t = copy.deepcopy(x)
                t[7] = s.area  # 区域
                t[8] = s.row  # 排
                t[9] = s.col  # 列

                # 全部转为字符串
                for i in range(len(t)):
                    t[i] =  '"{}"'.format( t[i] )
                t.append( s.id )

                output_seats.append(t)
            else:
                print('座位ID:{}不存在??'.format(x[0]))


    with open(output_csv_path, 'w') as outfile:
        # print(header)
        outfile.write(header + '\n')
        for row in output_seats:
            line = ','.join(row)
            outfile.write(line + '\n')
            # print(line)

    pass




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
