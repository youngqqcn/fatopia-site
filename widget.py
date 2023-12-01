# This Python file uses the following encoding: utf-8
import copy
import json
import sys
import os
import traceback
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtGui import   QIcon, QFont
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtWidgets import QApplication
from parse_data import Order, convert_solution_to_csv, output_csv_result, parse_order_data, parse_seats_data
from seats import arrange_seats_v1, check_seats

import subprocess

from ui_fantopia import Ui_Widget


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.setWindowTitle("Fantopia排座工具v1.1.0")
        self.setWindowIcon(QIcon('favicon.ico'))
        self.setFixedSize(self.width(), self.height())

        font = QFont()
        font.setPointSize(10)
        self.ui.teLog.setFont(font)


        # 按钮 订单座位表csv文件
        self.ui.btnOpenOrdersFile.clicked.connect( self.open_orders_file )
        self.ui.btnOpenAreaSeatsFile.clicked.connect(self.open_area_seats_file)

        # 开始排座
        self.ui.btnStartArrangeSeats.clicked.connect(self.start_arrange_seats)

        self.ui.leSpecialAreaRowSorts.textEdited.connect(self.handle_text_edited)
        self.ui.leAreaSorts.textEdited.connect(self.handle_text_edited)

        # 输出帮助信息
        self.show_help_message()
        pass

    def handle_text_edited(self, text):
        text = str(text).replace(' ', '').replace('\t', ' ').replace('\n', '').replace('\r', '')
        if self.sender() == self.ui.leSpecialAreaRowSorts:
            text = text.replace("'", '"')
            self.ui.leSpecialAreaRowSorts.setText(text)

        if self.sender() == self.ui.leAreaSorts:
            text = text.replace('"', '').replace("'", '')
            self.ui.leAreaSorts.setText(text)



    @staticmethod
    def show_help_message():
        """输出帮助信息"""

        print('====================================🔥使用说明🔥====================================')
        print('限制条件：')
        print('\t1) 只能针对同一票型(价格相同的票)进行排座, 如需处理不同票型,请分批处理')
        print('')
        print('⭐座位订单表csv文件: ')
        print('\t       来源:   是fantopia座位表导出结果, 请将xlsx转成csv文件')
        print('\t       字段:   座位ID,取票时间,票型ID,票型,用户ID,邮箱,订单,区域,排数,座位号')
        print('\t内容示例:   486017612198957,2023/11/25 10:00:00,129,PLATINUM SEATED,482654972404741,123456789@qq.com,486363947148933,,,')
        print('\n')
        print('⭐区域-排-座位号csv文件:')
        print('\t    来源:   由主办方提供, 请自行转为csv格式')
        print('\t字段名:   区域名称,排,座位号')
        print('\t    示例:   109,B,1')
        print('\n')
        print('⭐区域优先顺序: ')
        print('\t输入示例: 113, 114, 112, 111, 110, 109')
        print('\n')
        print('⭐特殊区域行排序: ')
        print('\t输入示例json格式: {"113":["C","B","D","A"], "109":["C","A","B"]}')
        print('\n')
        print('⭐订单分组间隔时间(秒): ')
        print('\t说明: 比如设置n秒, 订单排序算法如下:')
        print('\t\t第1步: 首先默认按照订单时间升序排序')
        print('\t\t第2步: 按照间隔n秒一组, 对所有订单进行分组')
        print('\t\t第3步: 对所有组进行组内排序, 同一组内按照订单的票数量进行降序排序, 即票多优先')
        print('==============================================================================')

        pass


    @staticmethod
    def open_file_dialog(parent):
        options = QFileDialog.Options()
        options |= QFileDialog.Option.ReadOnly

        file_dialog = QFileDialog(parent=parent)
        file_dialog.setOptions(options)

        # 只打开csv文件
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("CSV files (*.csv)")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            return file_path


    def open_orders_file(self):
        """打开订单表文件"""
        file_path = self.open_file_dialog(self)
        # self.ui.teLog.append( '文件路径:{}'.format( file_path ))

        if file_path is None or file_path == '':
            return

        if not os.path.exists(file_path):
            print( '文件不存在:{}'.format( file_path ))
            return

        print( '文件路径:{}'.format( file_path ))

        # 校验数据文件格式
        f = open(file_path, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        l = lines[0].split(',')
        header = '座位ID,取票时间,票型ID,票型,用户ID,邮箱,订单,区域,排数,座位号'
        h = header.split(',')
        for i in range(len(h)):
            assert h[i] in l
            assert l.index( h[i] ) == i , '{}!={},数据顺序不匹配'.format(l.index( h[i] ), i)  # 必须相同

        # 解析订单表文件
        self.orders = parse_order_data(file_path)

        print('{}, 解析成功!'.format(file_path))

        # 解析成功后再显示
        self.ui.leOrdersFilePath.setText(file_path)
        pass

    def open_area_seats_file(self):
        """打开座位表文件"""
        file_path = self.open_file_dialog(self)

        if file_path is None or file_path == '':
            return

        if not os.path.exists(file_path):
            print( '文件不存在:{}'.format( file_path ))
            return

        print( '文件路径:{}'.format( file_path ))

        # 校验数据文件格式
        f = open(file_path, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        l = lines[0].split(',')
        header = '区域名称,排,座位'
        h = header.split(',')
        for i in range(len(h)):
            assert h[i] in l
            assert l.index( h[i] ) == i , '{}!={},数据顺序不匹配'.format(l.index( h[i] ), i)  # 必须相同


        special_row_sorts_map = {}
        area_name = '' # 用于测试解析文件
        seats, row_index_name_map = parse_seats_data(path=file_path, area=area_name, special_row_sorts_map=special_row_sorts_map)

        print('{}, 解析成功!'.format(file_path))
        self.ui.leAreaSeatsFilePath.setText(file_path)
        pass

    def start_arrange_seats(self):
        """开始排座"""

        orders_csv_path =  self.ui.leOrdersFilePath.text().strip()
        area_seats_csv_path = self.ui.leAreaSeatsFilePath.text().strip()

        if orders_csv_path == '':
            QMessageBox.warning(self, '提示', '请选择"座位订单表csv文件"', QMessageBox.StandardButton.Ok)
            return
        if area_seats_csv_path  == '':
            QMessageBox.warning(self, '提示', '请选择"区域-排-座位号csv文件"', QMessageBox.StandardButton.Ok)
            return


        # 获取区域优先顺序
        tmp_sorts = self.ui.leAreaSorts.text().strip().split(',')
        areas_sorts = [ x for x in tmp_sorts if len(x) > 0]
        print('区域优先顺序:{}'.format(areas_sorts))
        if len(areas_sorts) == 0:
            QMessageBox.warning(self, '提示', '请输入区域优先顺序', QMessageBox.StandardButton.Ok)
            return


        # 获取特殊区域排(行)排序
        special_area_rows_sort_map = {}
        if True:
            try:
                sp = self.ui.leSpecialAreaRowSorts.text().strip()
                if len(sp) > 0 :
                    tmp = json.loads( sp )
                    assert isinstance(tmp, dict), '必须json对象,即{}'
                    if len(tmp) > 0:
                        assert isinstance(tmp[list(tmp.keys())[0]], list)
                    special_area_rows_sort_map = tmp
            except Exception as e:
                print('解析json错误信息:')
                traceback.print_exc()
                QMessageBox.warning(self, '错误', '区域内排(行)排序 解析错误, json格式错误', QMessageBox.StandardButton.Ok)
                return
        print('区域内排(行)排序: {}'.format( json.dumps(special_area_rows_sort_map) ))



        #================================================================
        # 获取订单分组间隔时间
        if True:
            order_group_gap_secs = self.ui.spinBoxOrderGroupGasSeconds.value()
            if order_group_gap_secs <= 0:
                order_group_gap_secs = 1

            # 设置间隔时间
            Order.ORDER_GROUP_GAP_SECONDS = order_group_gap_secs

        # 开始安排座位
        gloab_orders = parse_order_data(orders_csv_path)

        # 对订单排序
        gloab_orders = sorted(gloab_orders)

        # 备份原始订单, 方便后续操作
        backup_orders = copy.deepcopy(gloab_orders)

        # 检查座位数 和 订单座位数是否相等
        if True:

            all_total_seats_count = 0
            for a in areas_sorts:
                seats, row_index_name_map = parse_seats_data(path=area_seats_csv_path, area=a, special_row_sorts_map=special_area_rows_sort_map)
                # 统计该区可用座位数
                for r in range(len(seats)):
                    for c in  range(len(seats[r])):
                        if seats[r][c] == 'O':
                            all_total_seats_count += 1

            all_total_order_seats_count = 0
            for x in gloab_orders:
                all_total_order_seats_count += x.tix_count

            assert all_total_seats_count == all_total_order_seats_count , '总座位数和订单座位数不匹配,请检查数据文件'


        total_csv = {}
        for a in areas_sorts:
            seats, row_index_name_map = parse_seats_data(path=area_seats_csv_path, area=a, special_row_sorts_map=special_area_rows_sort_map)

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

            assert seats_count == 0, "区域座位不匹配"

            # 检查是否有不连座
            assert True == check_seats(new_seats), '结果无效,请检查'

            # 导出数据
            tmp_csv = convert_solution_to_csv(area=a, seats=seats, orders=backup_orders, row_index_name_map=row_index_name_map )

            # 合并
            total_csv.update(tmp_csv)

        # 输出csv
        print('===================')
        output_path = './排座结果.csv'
        output_csv_result(orders_csv_path, output_path, total_csv )
        print('===================')
        print('总座位数: {}'.format(len(total_csv)))
        print('输出结果文件: {}'.format(output_path))
        print('完成!')

        QMessageBox.information(self, '提示', '排座完成!', QMessageBox.StandardButton.Ok)
        if True:
            # 根据操作系统选择不同的命令
            if sys.platform.startswith('win'):
                command = 'explorer'
            elif sys.platform.startswith('darwin'):
                command = 'open'
            elif sys.platform.startswith('linux'):
                command = 'xdg-open'
            else:
                # raise OSError("Unsupported operating system")
                return

            # 执行命令打开文件管理器
            subprocess.run([command, os.getcwd()])
        pass





if __name__ == "__main__":
    exitCode = 0
    gApp = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    exitCode = gApp.exec()

    sys.exit(exitCode)