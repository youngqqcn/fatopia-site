#coding:utf8
#author: yqq
#date: 2023-11-30
#desc: 解析数据

import csv
import copy
import os
import pandas as pd

class Order:
    def __init__(self, id, raw_order_id, tix_count, tix_type, order_time, pay_time, seat_ids  ):
        self.id = id
        self.raw_order_id = raw_order_id
        self.tix_count = tix_count
        self.tix_type = tix_type
        self.order_time = order_time
        self.pay_time = pay_time
        self.seat_ids = seat_ids

        pass

    def __lt__(self, other):
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

    orders = []
    order_tix_count_map = {}
    order_info = []
    order_seatids_map = {}   # 订单id 和 座位id 映射

    with open(path, 'r') as file:
        reader = csv.reader(file)

        line = 0
        for row in reader:
            # 不解析首行
            if line == 0:
                line += 1
                continue

            order_id = row[6]
            if order_id not in order_tix_count_map:
                order_tix_count_map[order_id] = 1
                order_info.append( row )

                # 座位id
                order_seatids_map[order_id] = [ row[0] ]
            else:
                order_tix_count_map[order_id] += 1
                order_seatids_map[order_id].append( row[0] )

    # 将order用编号代替
    cur_ord_id = 1
    for o in order_info:
        order_id = o[6]
        ord = Order(id= '%03d'% cur_ord_id,
                    raw_order_id = order_id,
                    tix_count=order_tix_count_map[order_id],
                    order_time=o[2],
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
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for r in reader:
            # 过滤不是该区域的数据
            if r[0] != area: continue
            area_seats.append(r)

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
        print('file not exists , order_csv_path is {}'.format(order_csv_path))
        return
    else:
        print('文件存在')

    output_seats = [] # 保存当前区域的座位CSV原始数据
    header = ''
    with open(order_csv_path, 'r') as infile:

        lines = []
        raw_lines = infile.readlines()
        header = raw_lines[0].strip()
        for l in raw_lines[1:]:
            l = l.strip()
            lines.append(l.split(','))


        print('lines is {}'.format( len(lines)))
        for x in lines:
            # print('xxxxxxxxxxxxxxxxx')

            if x[0] in csv_data:
                s = csv_data[x[0]] # 已排座位信息

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

    print('all_seats len is {}'.format(len(output_seats)))

    with open(output_csv_path, 'w') as outfile:
        # w = csv.writer(outfile)
        # w.writerow( header.split(',') )
        outfile.write(header + '\n')
        for row in output_seats:
            line = ','.join(row)
            outfile.write(line + '\n')
            # w.writerow(row)

    # # 将csv转为 excel
    # data = pd.read_csv( output_csv_path )
    # # 创建 Excel 写入器
    # writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    # # 将数据写入 Excel 文件
    # data.to_excel(writer, index=False, sheet_name='Sheet1')
    # # 保存 Excel 文件
    # writer.close()




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
