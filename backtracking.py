#coding:utf8




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

def sort_by_time(ods):
    # 根据订单的时间排序, 默认是升序排序的
    # ods = sorted(ods, key=lambda o: o.create_time, reverse=False)
    return ods

def sort_by_tix_count(ods):
    """根据订单的票数排序"""
    # 按照订单降序排序
    r = sorted(ods, key=lambda o: o.tix_count, reverse=True)
    return r


stop_flag = False

def arrange_seats_v2(allseats, allords):

    # 先根据时间升序排序
    allords = sort_by_time(allords)

    # 再根据订单的票数降序排序
    allords = sort_by_tix_count(allords)
    # pprint(allords)


   # 统计可用座位数
    seats_count = 0
    for r in range(len(allseats)):
        for c in  range(len(allseats[r])):
            if allseats[r][c] == 'O':
                seats_count += 1

    order_seats_count = 0
    for o in allords:
        order_seats_count += o.tix_count

    if order_seats_count != seats_count:
        print('================== 座位数不匹配 =============')
        return


    global stop_flag
    stop_flag = False

    # 使用回溯，搜索所有可行方案
    def backtracking(ords):
        global stop_flag
        # 结束条件
        if len(ords) == 0:
            if check_seats(seats=allseats):
                print('======解:\n')
                # pprint(allseats)
                show_solution(allseats)
                stop_flag = True
            return

        for i in range(len(ords)):
            if stop_flag: return

            ord = ords[i]

            # 看看
            show_solution(allseats)

            found_flag = False
            found_flag, cur_row,start_col,end_col = seach_seats(allseats, ord.tix_count)

            # 如果没找到作为，返回
            if not found_flag:
                print('未找到 {}连座'.format(ord.tix_count))
                return

            # 如果找到了可排座位, 占座位row
            for x in range(start_col, end_col, -1):
                allseats[cur_row][x] = ord.id

            # 继续递归
            backtracking(ords[i+1:])

            # 撤销选择
            for x in range(start_col, end_col, -1):
                allseats[cur_row][x] = 'O'

    backtracking(ords=allords)
    pass



def seach_seats(a, count):
    cur_row = -100
    start_col = -100
    end_col = -109

    for row in range(len(a)): # 行，正序遍历
        for col in range(len(a[row]) - 1, -1, -1):  # 列， 逆向遍历
            if a[row][col] == 'X':
                continue
            if a[row][col] == 'O':
                if col - count >= -1 :
                    # 如果找到了可排座位, 占座位row
                    end_col = col - count
                    cur_row = row
                    start_col = col
                    return True, cur_row, start_col, end_col
    return False, cur_row, start_col, end_col

