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
        self.btnOpenOrdersFile.setGeometry(QRect(730, 10, 88, 25))
        self.leOrdersFilePath = QLineEdit(Widget)
        self.leOrdersFilePath.setObjectName(u"leOrdersFilePath")
        self.leOrdersFilePath.setGeometry(QRect(220, 10, 501, 25))
        self.leOrdersFilePath.setReadOnly(True)
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 10, 141, 17))
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 50, 161, 20))
        self.leAreaSeatsFilePath = QLineEdit(Widget)
        self.leAreaSeatsFilePath.setObjectName(u"leAreaSeatsFilePath")
        self.leAreaSeatsFilePath.setGeometry(QRect(220, 50, 501, 25))
        self.leAreaSeatsFilePath.setReadOnly(True)
        self.btnOpenAreaSeatsFile = QPushButton(Widget)
        self.btnOpenAreaSeatsFile.setObjectName(u"btnOpenAreaSeatsFile")
        self.btnOpenAreaSeatsFile.setGeometry(QRect(730, 50, 88, 25))
        self.btnStartArrangeSeats = QPushButton(Widget)
        self.btnStartArrangeSeats.setObjectName(u"btnStartArrangeSeats")
        self.btnStartArrangeSeats.setGeometry(QRect(890, 30, 131, 51))
        self.teLog = LogTextEdit(Widget)
        self.teLog.setObjectName(u"teLog")
        self.teLog.setGeometry(QRect(30, 180, 1091, 561))
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(100, 90, 101, 20))
        self.leAreaSorts = QLineEdit(Widget)
        self.leAreaSorts.setObjectName(u"leAreaSorts")
        self.leAreaSorts.setGeometry(QRect(220, 90, 501, 25))
        self.leSpecialAreaRowSorts = QLineEdit(Widget)
        self.leSpecialAreaRowSorts.setObjectName(u"leSpecialAreaRowSorts")
        self.leSpecialAreaRowSorts.setGeometry(QRect(220, 140, 511, 25))
        self.label_4 = QLabel(Widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(70, 140, 141, 17))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.btnOpenOrdersFile.setText(QCoreApplication.translate("Widget", u"\u9009\u62e9\u6587\u4ef6", None))
        self.leOrdersFilePath.setPlaceholderText(QCoreApplication.translate("Widget", u"\u53ea\u63a5\u53d7 .csv \u683c\u5f0f\u7684\u6587\u4ef6", None))
        self.label.setText(QCoreApplication.translate("Widget", u"\u5ea7\u4f4d\u8ba2\u5355\u8868csv\u6587\u4ef6", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"\u533a\u57df-\u6392-\u5ea7\u4f4d\u53f7csv\u6587\u4ef6", None))
        self.leAreaSeatsFilePath.setPlaceholderText(QCoreApplication.translate("Widget", u"\u53ea\u63a5\u53d7 .csv \u683c\u5f0f\u7684\u6587\u4ef6", None))
        self.btnOpenAreaSeatsFile.setText(QCoreApplication.translate("Widget", u"\u9009\u62e9\u6587\u4ef6", None))
        self.btnStartArrangeSeats.setText(QCoreApplication.translate("Widget", u"\u5f00\u59cb\u6392\u5ea7", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"\u533a\u57df\u4f18\u5148\u987a\u5e8f:", None))
        self.leAreaSorts.setPlaceholderText(QCoreApplication.translate("Widget", u"\u5fc5\u586b\u3002\u4ece\u597d\u5230\u5dee\u6392\u5e8f\u3002\u4ee5\u82f1\u6587\u9017\u53f7,\u5206\u9694", None))
        self.leSpecialAreaRowSorts.setPlaceholderText(QCoreApplication.translate("Widget", u"\u53ef\u9009\u3002Json\u683c\u5f0f\u3002\u5982\u4e0d\u6307\u5b9a\uff0c\u5219\u9ed8\u8ba4\u6309\u5b57\u6bcd(\u6216\u6570\u5b57)\u5347\u5e8f\u6392\u5e8f", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"\u533a\u57df\u5185\u6392(\u884c)\u6392\u5e8f:", None))
    # retranslateUi

