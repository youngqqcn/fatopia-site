#coding:utf8

# 根据这个，本问题是一个NP-Hard的问题，不存在多项式(时间)解
# https://stackoverflow.com/questions/8025931/allocating-contigous-seat-in-seat-map

# 可行方案：
#  使用回溯法搜寻所有方案
#  使用贪心算法, 但是可能不能达到最优方案


from pprint import pprint


def sort_by_time(ods):

    # 根据订单的时间排序
    ods = sorted(ods)



    return ods


def arrange_seats(seats, ords):
    """seats 是二维数组"""
    a = seats

    #根据时间排序
    ords = sort_by_time(ords)

    for ord in ords:
        def search():
            for row in range(len(a)):
                for col in range(len(a[0])):
                    if a[row][col] == '':
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
    # 使用贪心算法

    pass


def arrange_seats_v2(allseats, allords):

    # 使用回溯，搜索所有可行方案
    def backtracking(ords):
        # 结束条件
        if len(ords) == 0:
            if check_seats(seats=allseats):
                print('======解:\n')
                pprint(allseats)
            return


        for i in range(len(ords)):
            ord = ords[i]
            # 已经找不到可排座位
            row, start, end = search(allseats, ord.tix_count)
            if row == -1 or start == -1 or end == -1:
                return

            # 如果找到了可排座位, 占座位
            for x in range(start, end):
                # print('{} {}, x is {}'.format(start, end , x))
                allseats[row][x] = ord.id

            # 继续递归
            backtracking(ords[i+1:])

            # 撤销选择
            for x in range(start, end):
                allseats[row][x] = ''


    backtracking(ords=allords)
    pass


def search(a, tix_count):
    for row in range(len(a)):
        for col in range(len(a[row])):
            if a[row][col] == '':
                end = col + tix_count
                if end <= len(a[row]):
                    # print('len(a[row]) is {}'.format(len(a[row])))
                    return row, col, end
    # TODO: 如果没有找到合适的位置
    return -1, -1, -1



def check_seats(seats):
    """检查是否有不连座的"""
    row_map = {}
    for row in range(len(seats)):
        for col in range(len(seats[row])):
            id = seats[row][col]
            if id == '':
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




def test1():
    orders = [
        Order(id="1", tix_count= 1, tix_type= "VIP", order_time=12331, pay_time=12339),
        Order(id="2", tix_count= 2, tix_type= "VIP", order_time=12341, pay_time=12349),
        Order(id="3", tix_count= 3, tix_type= "VIP", order_time=12351, pay_time=12359),
        Order(id="4", tix_count= 3, tix_type= "VIP", order_time=12361, pay_time=12369),
        Order(id="5", tix_count= 2, tix_type= "VIP", order_time=12371, pay_time=12379),
        Order(id="6", tix_count= 2, tix_type= "VIP", order_time=12381, pay_time=12389),
        Order(id="7", tix_count= 3, tix_type= "VIP", order_time=12391, pay_time=12399),
        Order(id="8", tix_count= 1, tix_type= "VIP", order_time=12491, pay_time=12499),
        Order(id="9", tix_count= 1, tix_type= "VIP", order_time=12591, pay_time=12599),
    ]


    # 生成 3x6 的 的二维数组
    # seats = [['']*3]*6    # 这种方式有问题，内部用的引用，他妈的
    rows = 6
    cols = 3
    seats = [['' for _ in range(cols)] for _ in range(rows)]
    pprint(seats)

    # new_seats = arrange_seats(seats, orders)
    new_seats = arrange_seats_v2(seats, orders)

    print('===============\n\n')

    pprint(new_seats)
    pass


def main():
    test1()
    pass

if __name__ == '__main__':
    main()
