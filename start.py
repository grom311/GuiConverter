# -*- coding: utf-8 -*-
import threading
from PyQt5 import QtWidgets, QtGui
import ui.main as MainWindow
import subprocess, os,platform,datetime,base64,json
from urllib.request import urlopen
from PyQt5.QtGui import QIntValidator
from external.utils import Convert

FORMATS = ['jpg', 'webp', 'bmp']
SRC_EXTENTIONS = {
    'jpg': ['jpg', 'jpeg', 'jfif'],
    'heic': ['heic'],
}

class MyTool(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.img_path = resource_path('Icons/rose1.ico')
        self.setWindowIcon(QtGui.QIcon(self.img_path))
        self.fname = ''
        self.path_directory = ''
        self.res_convert = {}
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        stylesheet = """
        QPushButton#pushButton{
            background-color:#addfad;
        }
        QPushButton#pushButton_2{
            background-color:#addfad;
        }
        """
        self.setStyleSheet(stylesheet)
        self.onlyInt = QIntValidator()
        self.onlyInt_5 = QIntValidator()
        self.onlyInt_5.setRange(0, 100)

        self.ui.lineEdit_3.setValidator(self.onlyInt)
        self.ui.lineEdit_4.setValidator(self.onlyInt)
        # установить рэндж 0-100
        self.ui.lineEdit_5.setValidator(self.onlyInt_5)
        # self.ui.lineEdit.setText('E:/Foto/ROSE № 1/САЙТ/новый год 2025/101224/IMG_2478.HEIC')
        # self.ui.lineEdit_2.setText('E:/Temp/test__12')
        self.ui.comboBox.addItems(FORMATS)
        # self.ui.pushButton_2.setEnabled(False)
        # self.ui.pushButton.setEnabled(False)
        self.ui.pushButton.clicked.connect(self.run_clicked)
        self.ui.pushButton_2.clicked.connect(self.clear_options)
        self.ui.toolButton.clicked.connect(self.set_path)
        self.ui.toolButton_2.clicked.connect(self.set_path_2)
        self.ui.toolButton_3.clicked.connect(self.set_file_path)

# E:\Temp\img\img_src\024.JPG E:\Temp\img\res_qqqqqq\
    def convert_thread(self, height, width):
        self.res_convert = {'count': 0}
        for frm in SRC_EXTENTIONS.values():
            converter = Convert(
                self.ui.lineEdit.text(),
                self.ui.lineEdit_2.text(),
                int(self.ui.lineEdit_5.text()),
                (width, height),
                self.ui.comboBox.currentText(),
            )
            res_frm = converter.start_convert(frm)
            self.res_convert['count'] += res_frm['count']

    def run_clicked(self):
        lineedit_text = self.ui.lineEdit.text()
        lineedit2_text = self.ui.lineEdit_2.text()
        lineedit5_text = self.ui.lineEdit_5.text()
        if all([lineedit_text, lineedit2_text, lineedit5_text]):
            lineedit3_text = int(self.ui.lineEdit_3.text()) if self.ui.lineEdit_3.text() else None
            lineedit4_text = int(self.ui.lineEdit_4.text()) if self.ui.lineEdit_4.text() else None
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
            t = threading.Thread(
                name='convert-daemon',
                target=self.convert_thread,
                args=(lineedit4_text, lineedit3_text),
            )
            t.start()
            t.join()
            QtWidgets.QMessageBox.about(self, "Result convert", f'Count convert files: {self.res_convert["count"]}')
        else:
            QtWidgets.QMessageBox.about(self, "Options not correct", "Please insert all options")
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(True)

    def clear_options(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.setText('100')
        self.ui.comboBox.setCurrentIndex(0)

    def set_path(self):
        """Устанавливаем заданные пути для src folder."""
        res_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Results directory')
        if res_path != '':
            self.ui.lineEdit.setText(res_path)

    def set_file_path(self):
        """Устанавливаем путь для к файлу."""
        res_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Results directory')
        if res_path != '':
            self.ui.lineEdit.setText(res_path[0])

    def set_path_2(self):
        """Устанавливаем заданные пути для toolButton."""
        res_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Results directory')
        if res_path != '':
            self.ui.lineEdit_2.setText(res_path)


def resource_path(relative):

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    stylesheet = """
    QMainWindow{

    }
    QPushButton{
        background-color:#32cd32;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        border-color: beige;
        font: bold 14px;
        min-width: 4em;
        padding: 2px;
    }
    QPushButton:pressed {
        background-color: red;
        border-style: inset;
    }
    """
    app.setStyle('Fusion')
    window = MyTool()
    window.setWindowTitle('SFConverter')
    window.resize(600, 600)
    window.show()
    app.setStyleSheet(stylesheet)
    sys.exit(app.exec_())
