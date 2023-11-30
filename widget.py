# This Python file uses the following encoding: utf-8
import logging
import sys
import time
import os
from typing import List
from PySide6.QtWidgets import QApplication, QWidget, QAbstractItemView,QMessageBox
from PySide6.QtGui import QIntValidator,QDoubleValidator,QStandardItemModel, QRegularExpressionValidator
from PySide6.QtGui import  QStandardItem, QBrush, QColor, QIcon, QFont
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtCore import Qt,QThread, Signal, QTimer
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QApplication, QFileDialog, QDialog, QProgressBar, QVBoxLayout, QPushButton,QHeaderView
from traceback import print_exc

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QFontDatabase
from io import StringIO
from parse_data import parse_order_data, parse_seats_data


from ui_fantopia import Ui_Widget


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.setWindowTitle("Fantopia排座工具v1.0.0-2023-11-30")
        self.setWindowIcon(QIcon('favicon.ico'))
        self.setFixedSize(self.width(), self.height())

        font = QFont()
        font.setPointSize(10)
        self.ui.teLog.setFont(font)

        # 初始化
        self.orders = None
        self.seats = None
        self.row_index_name_map = None


        # 按钮 订单座位表csv文件
        self.ui.btnOpenOrdersFile.clicked.connect( self.open_orders_file )
        self.ui.btnOpenAreaSeatsFile.clicked.connect(self.open_area_seats_file)

        # 开始排座
        self.ui.btnStartArrangeSeats.clicked.connect(self.start_arrange_seats)

        print('====================================🔥使用说明🔥====================================')
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
        self.ui.leOrdersFilePath.setText(file_path)
        # self.ui.teLog.append( '文件路径:{}'.format( file_path ))

        if file_path is None or file_path == '':
            return

        if not os.path.exists(file_path):
            print( '文件不存在:{}'.format( file_path ))
            return

        print( '文件路径:{}'.format( file_path ))

        # 校验数据文件格式
        f = open(file_path, 'r')
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


        pass

    def open_area_seats_file(self):
        """打开座位表文件"""
        file_path = self.open_file_dialog(self)
        self.ui.leAreaSeatsFilePath.setText(file_path)

        if file_path is None or file_path == '':
            return

        if not os.path.exists(file_path):
            print( '文件不存在:{}'.format( file_path ))
            return

        print( '文件路径:{}'.format( file_path ))

        # 校验数据文件格式
        f = open(file_path, 'r')
        lines = f.readlines()
        f.close()
        l = lines[0].split(',')
        header = '区域名称,排,座位'
        h = header.split(',')
        for i in range(len(h)):
            assert h[i] in l
            assert l.index( h[i] ) == i , '{}!={},数据顺序不匹配'.format(l.index( h[i] ), i)  # 必须相同


        special_row_sorts_map = {}
        self.seats, self.row_index_name_map = parse_seats_data(path=file_path, area='114', special_row_sorts_map=special_row_sorts_map)

        print('{}, 解析成功!'.format(file_path))
        pass

    def start_arrange_seats(self):
        """开始排座"""

        if self.orders is None:
            QMessageBox.warning(self, '提示', '请选择"座位订单表csv文件"', QMessageBox.StandardButton.Ok)
            return
        if self.seats is None:
            QMessageBox.warning(self, '提示', '请选择"区域-排-座位号csv文件"', QMessageBox.StandardButton.Ok)
            return
        if self.row_index_name_map is None:
            QMessageBox.warning(self, '提示', '请输入"区域优先顺序"', QMessageBox.StandardButton.Ok)
            return


        areas_sorts = self.ui.leAreaSorts.text().strip()\
                        .replace("'", '').replace('"', '')\
                        .replace(' ', '').replace('\t', '').split(',')

        new_areas_sorts = [ x for x in areas_sorts if len(x) > 0]
        print('区域优先顺序:{}'.format(new_areas_sorts))
        if len(new_areas_sorts) == 0:
            QMessageBox.warning(self, '提示', '请输入区域优先顺序', QMessageBox.StandardButton.Ok)
            return


        pass




if __name__ == "__main__":
    exitCode = 0
    gApp = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    exitCode = gApp.exec()

    sys.exit(exitCode)