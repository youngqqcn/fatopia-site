# This Python file uses the following encoding: utf-8
import logging
import sys
import time
from typing import List
from PySide6.QtWidgets import QApplication, QWidget, QAbstractItemView,QMessageBox
from PySide6.QtGui import QIntValidator,QDoubleValidator,QStandardItemModel, QRegularExpressionValidator
from PySide6.QtGui import  QStandardItem, QBrush, QColor, QIcon
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtCore import Qt,QThread, Signal, QTimer
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QApplication, QFileDialog, QDialog, QProgressBar, QVBoxLayout, QPushButton,QHeaderView
from traceback import print_exc

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from io import StringIO


from ui_fantopia import Ui_Widget


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.setWindowTitle("Fantopia排座工具v1.0.0-2023-11-30")
        self.setWindowIcon(QIcon('favicon.ico'))
        self.setFixedSize(self.width(), self.height())


        # 按钮 订单座位表csv文件
        self.ui.btnOpenOrdersFile.clicked.connect( self.open_orders_file )
        self.ui.btnOpenAreaSeatsFile.clicked.connect(self.open_area_seats_file)

        # 开始排座
        self.ui.btnStartArrangeSeats.clicked.connect(self.start_arrange_seats)

        print('启动成功=============')
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

        self.ui.teLog.append( '文件路径:{}'.format( file_path ))

        pass

    def open_area_seats_file(self):
        """打开座位表文件"""
        file_path = self.open_file_dialog(self)
        self.ui.leAreaSeatsFilePath.setText(file_path)
        self.ui.teLog.append( '文件路径:{}'.format( file_path ))
        pass

    def start_arrange_seats(self):
        """开始排座"""


        pass




if __name__ == "__main__":
    exitCode = 0
    gApp = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    exitCode = gApp.exec()

    sys.exit(exitCode)