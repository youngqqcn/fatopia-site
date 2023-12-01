#coding:utf8


from pprint import pprint
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
        # orders = [
        #     Order(id="1", tix_count= 1, tix_type= "VIP", order_time=12331, pay_time=12339),
        #     Order(id="2", tix_count= 2, tix_type= "VIP", order_time=12341, pay_time=12349),
        #     Order(id="3", tix_count= 3, tix_type= "VIP", order_time=12351, pay_time=12359),
        #     Order(id="4", tix_count= 3, tix_type= "VIP", order_time=12361, pay_time=12369),
        #     Order(id="5", tix_count= 2, tix_type= "VIP", order_time=12371, pay_time=12379),
        #     Order(id="6", tix_count= 2, tix_type= "VIP", order_time=12381, pay_time=12389),
        #     Order(id="7", tix_count= 3, tix_type= "VIP", order_time=12391, pay_time=12399),
        #     Order(id="8", tix_count= 1, tix_type= "VIP", order_time=12491, pay_time=12499),
        #     Order(id="9", tix_count= 1, tix_type= "VIP", order_time=12591, pay_time=12599),
        # ]

        # 怎么排都不能连座
        # orders = [
        #     Order(id="1", tix_count= 3, tix_type= "VIP", order_time=12331, pay_time=12339),
        #     Order(id="2", tix_count= 3, tix_type= "VIP", order_time=12341, pay_time=12349),
        #     Order(id="3", tix_count= 3, tix_type= "VIP", order_time=12351, pay_time=12359),
        #     Order(id="4", tix_count= 3, tix_type= "VIP", order_time=12361, pay_time=12369),
        #     Order(id="5", tix_count= 2, tix_type= "VIP", order_time=12361, pay_time=12369),
        #     Order(id="6", tix_count= 2, tix_type= "VIP", order_time=12361, pay_time=12369),
        #     Order(id="7", tix_count= 2, tix_type= "VIP", order_time=12361, pay_time=12369),
        # ]

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




# 运行测试
if __name__ == '__main__':
    unittest.main()
