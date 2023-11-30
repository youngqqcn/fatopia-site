import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from io import StringIO

class LogTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

        # 将输出重定向到自定义的 QTextEdit 控件
        sys.stdout = self

    def write(self, text):
        # 将输出的文本追加到 QTextEdit 控件中
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)

        # 自动滚动到最后一行
        self.ensureCursorVisible()

app = QApplication([])
window = QMainWindow()
text_edit = LogTextEdit()
window.setCentralWidget(text_edit)
window.show()

print("Hello, world!")
print("This is a log message.")

app.exec()