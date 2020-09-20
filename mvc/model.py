import sys
import threading
import time

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QTextCursor

from ui_form import Ui_Form


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class Form(QMainWindow):
    finished = pyqtSignal()
    updateProgress = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # Install the custom output stream
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton_run.clicked.connect(self.start_task)
        self.finished.connect(self.end_task)
        self.updateProgress.connect(self.ui.progressBar.setValue)

    def start_task(self):

        self.thread = threading.Thread(target=self.run_test)
        self.thread.start()
        self.ui.pushButton_run.setEnabled(False)

    def end_task(self):
        self.ui.pushButton_run.setEnabled(True)

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        cursor = self.ui.textEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.ui.textEdit.setTextCursor(cursor)
        self.ui.textEdit.ensureCursorVisible()

    def run_test(self):
        for i in range(100):
            per = i + 1
            self.updateProgress.emit(per)
            # self.ui.progressBar.setValue(per)
            print("%%%s" % per)
            time.sleep(0.15)  # simulating expensive task

        print("Task Completed!")
        time.sleep(1.5)
        self.ui.progressBar.reset()
        self.finished.emit()


def main():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()