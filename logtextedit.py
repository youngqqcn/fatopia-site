# This Python file uses the following encoding: utf-8
# author: yqq
# date: 2023-11
# desc: 将标准输出，重定向到界面

import sys
from PySide6.QtWidgets import  QTextEdit
from PySide6.QtGui import QTextCursor


class LogTextEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # 将输出重定向到自定义的 QTextEdit 控件
        sys.stdout = self

    def write(self, text):
        # 将输出的文本追加到 QTextEdit 控件中
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)

        # 自动滚动到最后一行
        self.ensureCursorVisible()
