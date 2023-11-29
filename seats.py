#coding:utf8

# 根据这个，本问题是一个NP-Hard的问题，不存在多项式(时间)解
# https://stackoverflow.com/questions/8025931/allocating-contigous-seat-in-seat-map

# 可行方案：
#  使用回溯法搜寻所有方案
#  使用贪心算法, 但是可能不能达到最优方案


from pprint import pprint
from parse_data import Order
from parse_data import parse_order_data, parse_seats_data
import copy


def sort_by_time(ods):
    # 根据订单的时间排序, 默认是升序排序的
    # ods = sorted(ods, key=lambda o: o.create_time, reverse=False)
    return ods

def sort_by_tix_count(ods):
    """根据订单的票数排序"""
    # 按照订单降序排序
    r = sorted(ods, key=lambda o: o.tix_count, reverse=True)
    return r


def arrange_seats(seats, ords):
    """seats 是二维数组"""
    a = seats

    #根据时间排序
    ords = sort_by_time(ords)

    for ord in ords:
        def search():
            for row in range(len(a)):
                for col in range(len(a[0])):
                    if a[row][col] == 'O':
                        start_idx = col
                        end_idx = col + ord.tix_count
                        if end_idx <= len(a[0]):
                            for x in range(start_idx, end_idx):
                                a[row][x] = ord.id
                            return
            # TODO: 如果没有找到合适的位置
            pass
        search()
    return a



def arrange_seats_v1(seats, ords):
    # 假设 ords已经是按照最大订单排序
    ords = sort_by_tix_count(ords)

    orders_queue = copy.deepcopy( list(ords))

    # 使用贪心算法
    for row in range( len(seats) ):
        # 当前行剩余数量
        left_pos_count = 0
        for col in range(len(seats[0])):
            if seats[row][col] == 'O':
                left_pos_count += 1

        # 从订单列表中获取  最大且可安排的 的订单
        # copy_queue = copy.deepcopy( orders_queue)
        selected_ords = []
        for i in range(len(orders_queue)):
            o = orders_queue[i]

            # TODO: 假设中间都是连续的不间断的, 如果是间断的则用分治算法
            if o.tix_count <= left_pos_count:
                selected_ords.append(o)
                left_pos_count -= o.tix_count

        # 删除元素
        for o in selected_ords:
            orders_queue.remove(o)

        # 安排座位
        start_col = 0
        for o in selected_ords:
            for i in range(o.tix_count):
                if seats[row][start_col + i] == 'X':
                    print('============FUCK')
                seats[row][start_col + i] = o.id
            start_col += o.tix_count

    show_solution(seats)
    pass




def check_seats(seats):
    """检查是否有不连座的"""
    row_map = {}
    for row in range(len(seats)):
        for col in range(len(seats[row])):
            id = seats[row][col]
            if id == 'O':
                return False

            if id not in row_map:
                row_map[id] = set([row])
                continue
            else:
                row_map[id].add(row)

            # 如果存在不连座的
            if len(row_map[id]) > 2:
                return False
    return True


def show_solution(new_seats):
    print('===============')
    array = new_seats
    for r in range(len(array)):
        output = ''
        for c in range(len(array[0])):
            output += '{}'.format(array[r][c])
            if c != len(array[0]) - 1:
                output += ','
        print(output)
    print('===============')


def test1():
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
        Order(id="1", tix_count= 3, tix_type= "VIP", order_time=12331, pay_time=12339),
        Order(id="2", tix_count= 3, tix_type= "VIP", order_time=12341, pay_time=12349),
        Order(id="3", tix_count= 3, tix_type= "VIP", order_time=12351, pay_time=12359),
        Order(id="4", tix_count= 3, tix_type= "VIP", order_time=12361, pay_time=12369),
        Order(id="5", tix_count= 2, tix_type= "VIP", order_time=12361, pay_time=12369),
        Order(id="6", tix_count= 2, tix_type= "VIP", order_time=12361, pay_time=12369),
        Order(id="7", tix_count= 1, tix_type= "VIP", order_time=12361, pay_time=12369),
        Order(id="8", tix_count= 1, tix_type= "VIP", order_time=12361, pay_time=12369),
    ]


    # 生成 3x6 的 的二维数组
    # seats = [['']*3]*6    # 这种方式有问题，内部用的引用，他妈的
    rows = 6
    cols = 3
    seats = [['O' for _ in range(cols)] for _ in range(rows)]
    pprint(seats)

    # new_seats = arrange_seats(seats, orders)
    new_seats = arrange_seats(seats, orders)

    print('===============\n\n')

    pprint(new_seats)
    pass




def test2():


    arranged_ord_ids = set()
    # area_sorts = ['113', '114', '112', '111', '110', '109']
    area_sorts = ['113']
    for a in area_sorts:

        seats = parse_seats_data(path='./data/seats.csv', area=a)
        show_solution(seats)

        orders = parse_order_data('./data/order_data.csv')

        # 统计可用座位数
        seats_count = 0
        for r in range(len(seats)):
            for c in  range(len(seats[r])):
                if seats[r][c] == 'O':
                    seats_count += 1

        print('seats_count is {}'.format(seats_count))

        new_orders = []
        sum = 0
        for i in range(len(orders)):
            ord = orders[i]
            if ord.id in arranged_ord_ids:
                continue

            if sum + ord.tix_count == seats_count:
                new_orders.append(ord)
                arranged_ord_ids.add(ord.id)
                sum += ord.tix_count
                break
            elif sum + ord.tix_count > seats_count: # 当前的太大，往后找个小的来补充
                continue
            else:
                new_orders.append(ord)
                sum += ord.tix_count
                arranged_ord_ids.add(ord.id)

        if sum != seats_count:
            print('订单座位数和区域座位数作为不匹配========{}区,共{}笔订单,{}个座位, 但拿到sum:{}'.format(a, len(new_orders), seats_count, sum))
            return


        print('----------')
        print('{}区,共{}笔订单,{}个座位'.format(a, len(new_orders), seats_count))
        # pprint(new_orders)
        print('----------')

        new_seats = arrange_seats_v2(allseats=seats, allords=new_orders)
        print('===============\n\n')

    pass



def main():
    test1()
    # test2()
    pass

if __name__ == '__main__':
    main()
