from http.client import ACCEPTED
import sys

from hashlib import sha3_224
import rsa
import ast

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PyQt5.QtWidgets import QDesktopWidget, QPushButton, QFileDialog, QDialog, QTextEdit


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Digital signature'
        self.initUI()
    
    def initUI(self):
        self.resize(300, 120)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.setWindowTitle(self.title) 

        def sign():
            file = str(openFile()).encode('utf-8')
            (pubkey, privkey) = rsa.newkeys(512)
            hash = sha3_224(file)
            content = hash.digest()
            cipher = rsa.sign_hash(content, privkey, "SHA-224")
            saveFile(str(cipher))
            d = QDialog()
            d.setWindowTitle("Done")
            d.resize(300, 300)
            txt = QTextEdit(d)
            txt.resize(280, 240)
            txt.move(10, 10)
            txt.setReadOnly(True)
            txt.setText("Here is your private key. KEEP IT SAFE!\ns" + str(privkey.save_pkcs1("PEM")))
            btn = QPushButton("Noted", d)
            btn.resize(200, 30)
            btn.move(50, 260)
            btn.clicked.connect(d.accept)
            d.exec_()

        def validate():
            file = str(openFile()).encode('utf-8')
            signature = openFile()
            key = openFile()
            with key:
                keydata = key.read()
                privkey = rsa.PrivateKey.load_pkcs1(keydata, "PEM")
            if(check(file, signature, privkey)):
                d2 = QDialog()
                d2.setWindowTitle("I've checked it out")
                d2.resize(200, 100)
                txt2 = QTextEdit(d2)
                txt2.resize(180, 40)
                txt2.move(10, 10)
                txt2.setReadOnly(True)
                txt2.setText("Seems fine")
                btn2 = QPushButton("Yay", d2)
                btn2.resize(180, 30)
                btn2.move(10, 60)
                btn2.clicked.connect(d2.accept)
                d2.exec_()
            else:
                d2 = QDialog()
                d2.setWindowTitle("I've checked it out")
                d2.resize(200, 100)
                txt2 = QTextEdit(d2)
                txt2.resize(180, 40)
                txt2.move(10, 10)
                txt2.setReadOnly(True)
                txt2.setText("It doesn't lokk good")
                btn2 = QPushButton("Oh no", d2)
                btn2.resize(180, 30)
                btn2.move(10, 60)
                btn2.clicked.connect(d2.accept)
                d2.exec_()

        def openFile():
            filename = QFileDialog.getOpenFileName(self,'Open File')
            if filename[0]:
                f = open(filename[0],'r')
                return f

        def saveFile(content):
            filename = QFileDialog.getSaveFileName(self, "Save file", "", ".SIGNATURE")
            f = open(filename[0], 'w')
            f.write(content)
            f.close()

        def check(file, signature, key):
            hash = sha3_224(file)
            computed = rsa.decrypt(signature, key)
            if(hash == computed): return True
            return False

        buttonNewFile = QPushButton('Sign', self)
        buttonNewFile.setToolTip('Sign new file')
        buttonNewFile.resize(200, 30)
        buttonNewFile.move(50, 20)
        buttonNewFile.clicked.connect(sign)

        buttonOpenFile = QPushButton('Validate', self)
        buttonOpenFile.setToolTip('Validate file with existing signature')
        buttonOpenFile.resize(200, 30)
        buttonOpenFile.move(50, 60)
        buttonOpenFile.clicked.connect(validate)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())