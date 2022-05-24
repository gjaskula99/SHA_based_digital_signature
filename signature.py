from http.client import ACCEPTED
import sys

from hashlib import sha3_224
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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
        self.resize(300, 140)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.setWindowTitle(self.title) 

        def sign():
            file = str(openFile()).encode('utf-8')
            privkey = RSA.generate(2048, Random.new().read)
            pubkey = privkey.publickey()
            hash = sha3_224(file)
            content = hash.digest()
            cipher = PKCS1_OAEP.new(pubkey)
            M = cipher.encrypt(content)
            print(hash.hexdigest())
            print(M)
            saveFileBin(M, "Save signature")
            privkeySTR = privkey.export_key(format='PEM', passphrase=None, pkcs=1, protection=None, randfunc=None)

            def saveKey():
                filename = QFileDialog.getSaveFileName(self, "Save key file", "", ".PEM")
                f = open(filename[0], 'wb')
                f.write(privkeySTR)
                f.close()

            d = QDialog()
            d.setWindowTitle("Done")
            d.resize(300, 340)
            txt = QTextEdit(d)
            txt.resize(280, 240)
            txt.move(10, 10)
            txt.setReadOnly(True)
            txt.setText("Here is your private key. KEEP IT SAFE!\ns" + privkeySTR.decode("utf-8"))
            btn = QPushButton("Noted", d)
            btn.setToolTip('Make sure, I will not show it again')
            btn.resize(200, 30)
            btn.move(50, 260)
            btn.clicked.connect(d.accept)
            btn2 = QPushButton("Just save it", d)
            btn2.setToolTip('NO! IT"S NOT SAFE!!!')
            btn2.resize(200, 30)
            btn2.move(50, 300)
            btn2.clicked.connect(saveKey)
            d.exec_()

        def validate():
            file = str(openFile()).encode('utf-8')
            signature = openFileBin("Open signature file").read()
            privKey = openFileBin("Open key file").read()
            if(check(file, signature, privKey)):
                d2 = QDialog()
                d2.setWindowTitle("Checked")
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
                d2.setWindowTitle("Checked")
                d2.resize(200, 100)
                txt2 = QTextEdit(d2)
                txt2.resize(180, 40)
                txt2.move(10, 10)
                txt2.setReadOnly(True)
                txt2.setText("It doesn't look good")
                btn2 = QPushButton("Oh no", d2)
                btn2.resize(180, 30)
                btn2.move(10, 60)
                btn2.clicked.connect(d2.accept)
                d2.exec_()

        def openFile(desc="Open file"):
            filename = QFileDialog.getOpenFileName(self, desc)
            if filename[0]:
                f = open(filename[0],'r')
                return f

        def openFileBin(desc="Open file"):
            filename = QFileDialog.getOpenFileName(self, desc)
            if filename[0]:
                f = open(filename[0],'rb')
                return f

        def saveFile(content, desc="Save file"):
            filename = QFileDialog.getSaveFileName(self, desc, "", ".SIGNATURE")
            f = open(filename[0], 'w')
            f.write(content)
            f.close()

        def saveFileBin(content, desc="Save file"):
            filename = QFileDialog.getSaveFileName(self, desc, "", ".SIGNATURE")
            f = open(filename[0], 'wb')
            f.write(content)
            f.close()

        def check(file, signature, key):
            hash = sha3_224(file)
            privKey = RSA.importKey(key)
            cipher = PKCS1_OAEP.new(privKey)
            computed = cipher.decrypt(signature)
            print(hash.hexdigest())
            print(computed)
            if(hash.digest() == computed): return True
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

        buttonExit = QPushButton('Exit', self)
        buttonExit.setToolTip('Do I need to explain this functionality?')
        buttonExit.resize(200, 30)
        buttonExit.move(50, 100)
        buttonExit.clicked.connect(self.close)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
