#coding:utf8

# 根据这个，本问题是一个NP-Hard的问题，不存在多项式(时间)解
# https://stackoverflow.com/questions/8025931/allocating-contigous-seat-in-seat-map

# 可行方案：
#  使用回溯法搜寻所有方案
#  使用贪心算法, 但是可能不能达到最优方案


import copy



def arrange_seats_v1(area, seats, ords):
    """
    排座核心算法
    """

    # 假设 ords已经是按照最大订单排序
    # ords = sort_by_tix_count(ords)

    orders_queue = copy.deepcopy( list(ords))

    # 使用贪心算法
    for row in range( len(seats) ):
        # 当前行 总剩余数量
        current_row_total_left_pos_count = 0
        for col in range(len(seats[0])):
            if seats[row][col] == 'O':
                current_row_total_left_pos_count += 1

        # 列游标
        column_cursor_start_index = 0

        loop_count = 0
        # 搞这么复杂是为了处理中间间断了的情况, 例如： O,O,O,X,X,O,O,O,X  就有2个可用区间
        while current_row_total_left_pos_count > 0 :
            loop_count += 1
            if loop_count > 10000:
                raise Exception("卧槽, 死循环了!")

            # 当前连续区间剩余座位数
            cur_continious_left_pos_count = 0
            for col in range(column_cursor_start_index, len(seats[0])):
                if seats[row][col] == 'O':
                    cur_continious_left_pos_count += 1
                if seats[row][col] == 'X':
                    break

            # 从订单列表中获取  最大且可安排的 的订单
            selected_ords = []
            for i in range(len(orders_queue)):
                o = orders_queue[i]

                if o.tix_count <= cur_continious_left_pos_count:
                    selected_ords.append(o)
                    # 当前连续区间的可用数，减少
                    cur_continious_left_pos_count -= o.tix_count
                    # 当前行总的可座位数,减少
                    current_row_total_left_pos_count -= o.tix_count

            # 如果没有找到合适的订单
            if cur_continious_left_pos_count != 0:
                raise Exception('======!不可排座,请调整"订单分组间隔时间"后再试')

            # 删除元素
            for o in selected_ords:
                orders_queue.remove(o)

            # 安排座位
            start_col = column_cursor_start_index
            for o in selected_ords:
                for i in range(o.tix_count):
                    if seats[row][start_col + i] == 'X':
                        raise Exception("====FUCK======")
                    seats[row][start_col + i] = o.id
                start_col += o.tix_count

            # 如果后面还有可用的， 把 column_cursor_index 移到下一个可用区间的开头
            if current_row_total_left_pos_count > 0:
                while column_cursor_start_index < len(seats[0]) :
                    if seats[row][column_cursor_start_index] == 'O':
                        break # while
                    column_cursor_start_index += 1

            print('=========> current_row_total_left_pos_count = {}'.format(current_row_total_left_pos_count))
            print('=========> column_cursor_start_index = {}'.format(column_cursor_start_index))
            print('=========> row = {}'.format(row))
            show_solution(area, seats)
            pass



    # 打印结果
    show_solution(area, seats)

    return seats, orders_queue





def check_seats(seats):
    """检查是否有不连座的"""

    row_map = {}
    for row in range(len(seats)):
        col_map = {}
        for col in range(len(seats[row])):
            id = seats[row][col]
            if id == 'X': continue
            if id == 'O':
                print('有空位置: {}行{}列'.format(row, col))
                return False
            if id not in row_map:
                row_map[id] = set([row])
                col_map[id] = [col]
                continue
            else:
                row_map[id].add(row)
                col_map[id].append(col)
            # 如果存在不同排的
            if len(row_map[id]) > 2:
                print('存在不连座： id:{}, row_map[id]:{}'.format(id, row_map[id]))
                return False

        # 检查是否有不连座的
        for k, cols in col_map.items():
            for i in range(len(cols) - 1):
                if cols[i + 1] - cols[i] > 1:
                    print('id:{}有不连座的情况, 请检查'.format(k))
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

