# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fantopia.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

from logtextedit import LogTextEdit

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1150, 764)
        self.btnOpenOrdersFile = QPushButton(Widget)
        self.btnOpenOrdersFile.setObjectName(u"btnOpenOrdersFile")
        self.btnOpenOrdersFile.setGeometry(QRect(650, 10, 88, 25))
        self.leOrdersFilePath = QLineEdit(Widget)
        self.leOrdersFilePath.setObjectName(u"leOrdersFilePath")
        self.leOrdersFilePath.setGeometry(QRect(150, 10, 481, 25))
        self.leOrdersFilePath.setReadOnly(True)
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 10, 111, 17))
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 50, 121, 16))
        self.leAreaSeatsFilePath = QLineEdit(Widget)
        self.leAreaSeatsFilePath.setObjectName(u"leAreaSeatsFilePath")
        self.leAreaSeatsFilePath.setGeometry(QRect(150, 50, 481, 25))
        self.btnOpenAreaSeatsFile = QPushButton(Widget)
        self.btnOpenAreaSeatsFile.setObjectName(u"btnOpenAreaSeatsFile")
        self.btnOpenAreaSeatsFile.setGeometry(QRect(650, 50, 88, 25))
        self.btnStartArrangeSeats = QPushButton(Widget)
        self.btnStartArrangeSeats.setObjectName(u"btnStartArrangeSeats")
        self.btnStartArrangeSeats.setGeometry(QRect(830, 10, 131, 51))
        self.teLog = LogTextEdit(Widget)
        self.teLog.setObjectName(u"teLog")
        self.teLog.setGeometry(QRect(30, 120, 1091, 621))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.btnOpenOrdersFile.setText(QCoreApplication.translate("Widget", u"\u9009\u62e9\u6587\u4ef6", None))
        self.label.setText(QCoreApplication.translate("Widget", u"\u8ba2\u5355\u5ea7\u4f4dcsv\u6587\u4ef6", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"\u533a\u57df\u5ea7\u4f4dcsv\u6587\u4ef6", None))
        self.btnOpenAreaSeatsFile.setText(QCoreApplication.translate("Widget", u"\u9009\u62e9\u6587\u4ef6", None))
        self.btnStartArrangeSeats.setText(QCoreApplication.translate("Widget", u"\u5f00\u59cb\u6392\u5ea7", None))
    # retranslateUi

