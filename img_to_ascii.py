import os
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QFileDialog, \
    QVBoxLayout, QLineEdit, QMessageBox, QGroupBox, QGridLayout, QTextEdit, QDialog, QCheckBox, QAction
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from tkinter import messagebox


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def initUI(self):

        grid = QGridLayout()
        grid.addWidget(self.saveInfoGroup(), 0, 0)

        self.setLayout(grid)

        self.setWindowTitle('Image to ASCII')
        self.resize(300, 150)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def saveInfoGroup(self):
        global nw, w_num, checkInvert, saveCheckInvert
        nw = ''
        checkInvert = False
        saveCheckInvert = False

        groupbox = QGroupBox('')

        btn1 = QPushButton("적용할 이미지", self)
        btn1.clicked.connect(self.openFileNameDialog)

        w_num = QLineEdit(self)
        w_num.setPlaceholderText('가로 크기 (기본 50)')
        w_num.textChanged.connect(self.nwInput)

        btn2 = QCheckBox('반전', self)
        btn2.stateChanged.connect(self.invert)

        saveBtn = QCheckBox('메모장으로 저장', self)
        saveBtn.stateChanged.connect(self.saveInvert)

        btn3 = QPushButton("아스키코드 변환", self)
        btn3.clicked.connect(self.textGroup)

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(w_num)
        vbox.addWidget(btn2)
        vbox.addWidget(saveBtn)
        vbox.addWidget(btn3)
        groupbox.setLayout(vbox)

        return groupbox

    def nwInput(self, text):
        global nw
        nw = text

    def openFileNameDialog(self):
        global img, fileName

        filePath, _ = QFileDialog.getOpenFileName(self, "적용할 이미지를 선택하세요.", "")
        fileName = QFileInfo(filePath).fileName()

        if filePath:
            img = cv2.imread(filePath)
            try:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            except:
                QMessageBox.critical(self, 'Message', '이미지 파일이 아니거나\n이미지 경로에 한글이 들어가 있습니다.\n' + filePath,
                                     QMessageBox.Yes)
                return

    def invert(self, state):
        global checkInvert
        if state == Qt.Checked:
            checkInvert = True
        else:
            checkInvert = False

    def saveInvert(self, state):
        global saveCheckInvert
        if state == Qt.Checked:
            saveCheckInvert = True
        else:
            saveCheckInvert = False

    def textGroup(self):
        global result

        self.dialog = QDialog()
        self.dialog.setWindowTitle('결과')
        self.dialog.setWindowModality(Qt.ApplicationModal)

        try:
            h, w = img.shape
        except:
            QMessageBox.critical(self, 'Message', '이미지 파일을 선택해 주세요.',
                                 QMessageBox.Yes)
            return

        if nw == '':
            nh = int(h / w * 50)
            reImg = cv2.resize(img, (50 * 2, nh))
            self.dialog.resize(550, (nh * 10 + 150))
        else:
            try:
                nh = int(h / w * int(nw))
                reImg = cv2.resize(img, (int(nw) * 2, nh))
                self.dialog.resize((int(nw) * 10 + 50), (nh * 10 + 150))
            except:
                QMessageBox.critical(self, 'Message', '숫자만 입력해 주세요.',
                                     QMessageBox.Yes)
                w_num.setText('')
                return

        textBox = QTextEdit('')
        fontDB = QFontDatabase()
        fontDB.addApplicationFont(self.resource_path('./font/CascadiaCode.ttf'))
        fontVar = QFont("Cascadia Code", 7)
        textBox.setCurrentFont(fontVar)
        box = QVBoxLayout()
        box.addWidget(textBox)

        result = ''

        if checkInvert:
            CHARS = '@$#*!=;:~-,. '
        else:
            CHARS = ' .,-~:;=!*#$@'

        for row in reImg:
            text = ''
            for pixel in row:
                index = int(pixel / 256 * len(CHARS))
                text += CHARS[index]

            result += text + '\n'
        print(result)
        textBox.append(result)

        if saveCheckInvert:
            saveFileName = fileName + "_ASCII.txt"

            File = open(saveFileName, "w")
            print(result, file=File)

            QMessageBox.information(self, 'Message', '파일 저장 완료\n' + saveFileName,
                                    QMessageBox.Yes)


        self.dialog.setLayout(box)
        self.dialog.show()

    def saveTxt(self):
        try:
            saveFileName = fileName+"_ASCII.txt"
        except:
            QMessageBox.critical(self, 'Message', '이미지 파일을 선택해 주세요.',
                                 QMessageBox.Yes)
            return

        File = open(saveFileName, "w")
        print(result, file=File)

        QMessageBox.information(self, 'Message', '파일 저장 완료\n'+saveFileName,
                             QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
