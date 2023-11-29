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


# gloab_orders = parse_order_data('./data/order_data.csv')


def sort_by_time(ods):
    # 根据订单的时间排序, 默认是升序排序的
    # ods = sorted(ods, key=lambda o: o.create_time, reverse=False)
    return ods

def sort_by_tix_count(ods):
    """根据订单的票数排序"""
    # 按照订单降序排序
    # ods = sorted(ods, key=lambda o: o.tix_count, reverse=True)
    return ods


def arrange_seats_v1(area, seats, ords):
    # 假设 ords已经是按照最大订单排序
    # ords = sort_by_tix_count(ords)

    orders_queue = copy.deepcopy( list(ords))

    # 使用贪心算法
    for row in range( len(seats) ):
        # 当前行剩余数量
        left_pos_count = 0
        for col in range(len(seats[0])):
            if seats[row][col] == 'O':
                left_pos_count += 1

        # 从订单列表中获取  最大且可安排的 的订单
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
                    raise Exception("====FUCK======")
                seats[row][start_col + i] = o.id
            start_col += o.tix_count

    # 打印结果
    show_solution(area, seats)

    return seats, orders_queue


def convert_solution_to_csv(area, seats, orders, row_index_name_map,  outfile):

    # 将orders转为 以order.id 为key的dict
    orders_map = { ord.id :  ord for ord in orders   }


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

            line = '{},{},{},{},{}\n'.format(id, seat_id, area, row_index_name_map[row], col)
            # print(line.strip())
            outfile.write(line)
    pass


def check_seats(seats):
    """检查是否有不连座的"""
    #TODO: 检查是否有漏

    row_map = {}
    for row in range(len(seats)):
        for col in range(len(seats[row])):
            id = seats[row][col]
            if id == 'X': continue
            if id == 'O':
                print('有空位置')
                return False

            if id not in row_map:
                row_map[id] = set([row])
                continue
            else:
                row_map[id].add(row)

            # 如果存在不连座的
            if len(row_map[id]) > 2:
                print('存在不连座： id:{}, row_map[id]:{}'.format(id, row_map[id]))
                return False
    return True


def show_solution(area, new_seats):
    """打印排座结果"""

    print('{}区排座如下：'.format(area))
    array = new_seats
    for r in range(len(array)):
        output = ''
        for c in range(len(array[0])):
            output += '{}'.format(array[r][c])
            if c != len(array[0]) - 1:
                output += ','
        print(output)

