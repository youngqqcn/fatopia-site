#coding:utf8


from datetime import datetime, timedelta
from pprint import pprint
import random
import traceback
import unittest

from parse_data import Order, convert_solution_to_csv, output_csv_result, parse_order_data, parse_seats_data
from seats import arrange_seats_v1, check_seats
import copy

# 编写测试类
class TestAddNumbers(unittest.TestCase):

    def test_arrange_seats_v1(self):

        # Order.ORDER_GROUP_GAP_SECONDS = 666

        gloab_orders = parse_order_data('./data/order_data.csv')
        backup_orders = copy.deepcopy(gloab_orders)

        # 区域顺序
        area_sorts = ['113', '114', '112', '111', '110', '109']

        # 行顺序, 如果不设置，就按照字母顺序
        special_row_sorts_map = {
            '109': ['G','H','J','K', 'L', 'M', 'N', 'P', 'Q', 'B', 'C']
        }

        total_csv = {}
        for a in area_sorts:
            seats, row_index_name_map = parse_seats_data(path='./data/seats.csv', area=a, special_row_sorts_map=special_row_sorts_map)

            # 统计可用座位数
            seats_count = 0
            for r in range(len(seats)):
                for c in  range(len(seats[r])):
                    if seats[r][c] == 'O':
                        seats_count += 1

            print()
            print('剩余{}笔订单,{}区,{}个座位'.format(a, len(gloab_orders), seats_count))

            new_seats, gloab_orders = arrange_seats_v1(area=a, seats=seats, ords=gloab_orders)

            # 检查区域的座位数是否匹配
            for r in range(len(seats)):
                for c in  range(len(seats[r])):
                    if seats[r][c] != 'X' :
                        seats_count -= 1

            self.assertEqual(seats_count, 0, "区域座位不匹配")

            # 检查是否有不连座
            self.assertTrue( check_seats(new_seats), '结果无效,请检查')

            # 导出数据
            tmp_csv = convert_solution_to_csv(area=a, seats=seats, orders=backup_orders, row_index_name_map=row_index_name_map )

            # 合并
            total_csv.update(tmp_csv)

        # 输出csv
        print('total len is {}'.format(len(total_csv)))
        output_path = './data/排座结果.csv'
        output_csv_result('./data/order_data.csv', output_path, total_csv )
        pass



    def test_arrange_seats(self):
        # 可以连座
        orders = [
            Order(id="1", raw_order_id='1', tix_count= 3, tix_type= "VIP", order_time=12331, pay_time=12339, seat_ids=[1]),
            Order(id="2", raw_order_id='2', tix_count= 3, tix_type= "VIP", order_time=12341, pay_time=12349, seat_ids=[2]),
            Order(id="3", raw_order_id='3', tix_count= 3, tix_type= "VIP", order_time=12351, pay_time=12359, seat_ids=[3]),
            Order(id="4", raw_order_id='4', tix_count= 3, tix_type= "VIP", order_time=12361, pay_time=12369, seat_ids=[4]),
            Order(id="5", raw_order_id='5', tix_count= 2, tix_type= "VIP", order_time=12361, pay_time=12369, seat_ids=[5]),
            Order(id="6", raw_order_id='6', tix_count= 2, tix_type= "VIP", order_time=12361, pay_time=12369, seat_ids=[6]),
            Order(id="7", raw_order_id='7', tix_count= 1, tix_type= "VIP", order_time=12361, pay_time=12369, seat_ids=[7]),
            Order(id="8", raw_order_id='8', tix_count= 1, tix_type= "VIP", order_time=12361, pay_time=12369, seat_ids=[8]),
        ]


        # 生成 3x6 的 的二维数组
        # seats = [['']*3]*6    # 这种方式有问题，内部用的引用，他妈的
        rows = 6
        cols = 3
        seats = [['O' for _ in range(cols)] for _ in range(rows)]

        arrange_seats_v1('A', seats, orders)

        pass


    def test_orders_sort(self):
        orders = [
            Order(id="1", raw_order_id='1', tix_count= 1, tix_type= "VIP", order_time=1, pay_time=0, seat_ids=[1]),
            Order(id="2", raw_order_id='2', tix_count= 3, tix_type= "VIP", order_time=66, pay_time=0, seat_ids=[2]),
            Order(id="3", raw_order_id='3', tix_count= 9, tix_type= "VIP", order_time=100, pay_time=0, seat_ids=[3]),
            Order(id="4", raw_order_id='4', tix_count= 3, tix_type= "VIP", order_time=2, pay_time=0, seat_ids=[4]),
            Order(id="5", raw_order_id='5', tix_count= 2, tix_type= "VIP", order_time=6, pay_time=0, seat_ids=[5]),
            Order(id="6", raw_order_id='6', tix_count= 4, tix_type= "VIP", order_time=9, pay_time=0, seat_ids=[6]),
            Order(id="7", raw_order_id='7', tix_count= 5, tix_type= "VIP", order_time=8, pay_time=0, seat_ids=[7]),
            Order(id="8", raw_order_id='8', tix_count= 6, tix_type= "VIP", order_time=7, pay_time=0, seat_ids=[8]),
        ]

        ords = sorted(orders)
        pprint(ords)

        pass

    def test_arrange_seats_v2(self):
        """测试增加间隔时间"""

        success_flag = False
        # 自动调整间隔时间, 解决那些不可能排座的情况
        for i in range(1, 5000):
            Order.ORDER_GROUP_GAP_SECONDS = i
            orders = [
                Order(id="6", raw_order_id='6', tix_count= 1, tix_type= "VIP", order_time=12031, pay_time=12369, seat_ids=[6]),
                Order(id="9", raw_order_id='6', tix_count= 1, tix_type= "VIP", order_time=12031, pay_time=12369, seat_ids=[6]),
                Order(id="7", raw_order_id='6', tix_count= 1, tix_type= "VIP", order_time=12031, pay_time=12369, seat_ids=[6]),
                Order(id="1", raw_order_id='1', tix_count= 3, tix_type= "VIP", order_time=12331, pay_time=12339, seat_ids=[1]),
                Order(id="2", raw_order_id='2', tix_count= 2, tix_type= "VIP", order_time=12341, pay_time=12349, seat_ids=[2]),
                Order(id="3", raw_order_id='3', tix_count= 3, tix_type= "VIP", order_time=12351, pay_time=12359, seat_ids=[3]),
                Order(id="4", raw_order_id='4', tix_count= 3, tix_type= "VIP", order_time=12361, pay_time=12369, seat_ids=[4]),
                Order(id="5", raw_order_id='5', tix_count= 2, tix_type= "VIP", order_time=12371, pay_time=12369, seat_ids=[5]),
                Order(id="8", raw_order_id='7', tix_count= 2, tix_type= "VIP", order_time=12381, pay_time=12369, seat_ids=[7]),
            ]
            orders = sorted(orders)

            # 生成 3x6 的 的二维数组
            # seats = [['']*3]*6    # 这种方式有问题，内部用的引用，他妈的
            seats = [
                ['O', 'O', 'O'],
                ['O', 'O', 'O'],
                ['O', 'O', 'O'],
                ['O', 'O', 'O'],
                ['O', 'O', 'O'],
                ['O', 'O', 'O']
            ]

            try:
                arrange_seats_v1('A', seats, orders)

                # 一切正常则继续
                print('订单分组间隔时间: {}'.format(i))

                success_flag = True

                break
            except Exception as e:
                print('继续')
                continue

        self.assertTrue(success_flag)

    def test_arrange_seats_v3(self):
        """测试一行中间有间断"""

        success_flag = False
        # 自动调整间隔时间, 解决那些不可能排座的情况
        for i in range(1, 5000):
            Order.ORDER_GROUP_GAP_SECONDS = i
            orders = [
                Order(id="6", raw_order_id='6', tix_count= 1, tix_type= "VIP", order_time=12031, pay_time=12369, seat_ids=[6]),
                Order(id="9", raw_order_id='6', tix_count= 1, tix_type= "VIP", order_time=12031, pay_time=12369, seat_ids=[6]),
                Order(id="7", raw_order_id='6', tix_count= 1, tix_type= "VIP", order_time=12031, pay_time=12369, seat_ids=[6]),
                Order(id="1", raw_order_id='1', tix_count= 3, tix_type= "VIP", order_time=12331, pay_time=12339, seat_ids=[1]),
                Order(id="2", raw_order_id='2', tix_count= 2, tix_type= "VIP", order_time=12341, pay_time=12349, seat_ids=[2]),
                Order(id="3", raw_order_id='3', tix_count= 3, tix_type= "VIP", order_time=12351, pay_time=12359, seat_ids=[3]),
                Order(id="4", raw_order_id='4', tix_count= 3, tix_type= "VIP", order_time=12361, pay_time=12369, seat_ids=[4]),
                Order(id="5", raw_order_id='5', tix_count= 2, tix_type= "VIP", order_time=12371, pay_time=12369, seat_ids=[5]),
                # Order(id="8", raw_order_id='7', tix_count= 2, tix_type= "VIP", order_time=12381, pay_time=12369, seat_ids=[7]),
            ]
            orders = sorted(orders)


            # 生成 3x6 的 的二维数组
            # seats = [['']*3]*6    # 这种方式有问题，内部用的引用，他妈的
            seats = [
                ['O', 'X', 'O'],
                ['X', 'O', 'O'],
                ['O', 'O', 'O'],
                ['O', 'O', 'O'],
                ['O', 'O', 'O'],
                ['O', 'O', 'O']
            ]

            try:
                arrange_seats_v1('A', seats, orders)

                # 一切正常则继续
                print('订单分组间隔时间: {}'.format(i))

                success_flag = True

                break
            except Exception as e:
                traceback.print_exc()
                continue

        self.assertTrue(success_flag)



    def test_make_dummy_order_time(self):

        with open('./data/order_data.csv', 'r') as infile , open('./data/dummy_order_data.csv', 'w') as outfile:
            alllines = infile.readlines()
            outfile.write(alllines[0] )
            alllines = alllines[1:]
            line_count = 1
            orders = {}
            for line in alllines:
                line = line.strip()
                line = line.split(',')
                ord_time = line[1]

                ord_id = line[6]
                if ord_id not in orders:
                    ord_ts = datetime.strptime(ord_time, '%Y/%m/%d %H:%M:%S')
                    ord_ts += timedelta(seconds=line_count)
                    new_ord_time = ord_ts.strftime('%Y/%m/%d %H:%M:%S')
                    orders[ord_id] = new_ord_time

                line[1] = orders[ord_id]

                # line = ','.join(line)

                for n in range(len(line)):
                    line[n] = "'{}'".format(line[n])


                output  = ','.join(line)
                outfile.write(output  + '\n')
                line_count += 1




        pass






# 运行测试
if __name__ == '__main__':
    unittest.main()
