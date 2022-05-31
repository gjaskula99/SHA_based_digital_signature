import sys

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA3_224

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QDesktopWidget, QPushButton, QFileDialog, QDialog, QTextEdit


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Digital signature'
        self.initUI()
    
    def initUI(self):
        self.resize(300, 180)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.setWindowTitle(self.title) 

        #Functions
        def errorDialog(text = "Sorry, something went wrong"):
            d = QDialog()
            d.setWindowTitle("Error")
            d.resize(200, 100)
            txt = QTextEdit(d)
            txt.resize(180, 40)
            txt.move(10, 10)
            txt.setReadOnly(True)
            txt.setText(text)
            btn = QPushButton("Oh no", d)
            btn.setToolTip('Anyway')
            btn.resize(180, 30)
            btn.move(10, 60)
            btn.clicked.connect(d.accept)
            d.exec_()

        def openFile(desc="Open file"):
            filename = QFileDialog.getOpenFileName(self, desc)
            if filename[0]:
                f = open(filename[0],'r')
                return f
            raise IOError("No file selected")

        def openFileBin(desc="Open file"):
            filename = QFileDialog.getOpenFileName(self, desc)
            if filename[0]:
                f = open(filename[0],'rb')
                return f
            raise IOError("No file selected")

        def saveFile(content, desc="Save file"):
            filename = QFileDialog.getSaveFileName(self, desc, "", ".SIGNATURE")
            if filename[0]:
                f = open(filename[0], 'w')
                f.write(content)
                f.close()
                return
            raise IOError("No file selected")

        def saveFileBin(content, desc="Save file"):
            filename = QFileDialog.getSaveFileName(self, desc, "", ".SIGNATURE")
            if filename[0]:
                f = open(filename[0], 'wb')
                f.write(content)
                f.close()
                return
            raise IOError("No file selected")

        def check(file, signature, key):
            try:
                hash = SHA3_224.new(file)
                print(hash.hexdigest())
                verifier = pss.new(key)
                verifier.verify(hash, signature)
                return True
            except:
                errorDialog("Signature is not valid")
                return False

        #Signing itself
        def sign():
            errorFlag = False
            try:
                file = str(openFile()).encode('utf-8')
            except:
                errorFlag = True
                errorDialog("No file chosen for opening")
            if(not errorFlag):
                keys = RSA.generate(2048, Random.new().read)
                pubkey = keys.publickey()
                hash = SHA3_224.new(file)
                cipher = pss.new(keys).sign(hash)
                print(hash.hexdigest())
                print(cipher)
                try:
                    saveFileBin(cipher, "Save signature")
                except:
                    errorFlag = True
                    errorDialog("File saving aborted by user")
                keySTR = pubkey.export_key(format='PEM', passphrase=None, pkcs=1, protection=None, randfunc=None)

                def saveKey():
                    filename = QFileDialog.getSaveFileName(self, "Save key file", "", ".PEM")
                    try:
                        if not filename[0]: raise IOError("No file selected")
                        f = open(filename[0], 'wb')
                        f.write(keySTR)
                        f.close()
                    except:
                        errorFlag = True
                        errorDialog("File saving aborted by user")
            
            if(not errorFlag):
                d = QDialog()
                d.setWindowTitle("Done")
                d.resize(300, 340)
                txt = QTextEdit(d)
                txt.resize(280, 240)
                txt.move(10, 10)
                txt.setReadOnly(True)
                txt.setText("Here is your private key. KEEP IT SAFE!\n" + keySTR.decode("utf-8"))
                btn = QPushButton("Noted", d)
                btn.setToolTip('Make sure, I will not show it again')
                btn.resize(200, 30)
                btn.move(50, 260)
                btn.clicked.connect(d.accept)
                btn2 = QPushButton("Just save it", d)
                btn2.setToolTip('To file?')
                btn2.resize(200, 30)
                btn2.move(50, 300)
                btn2.clicked.connect(saveKey)
                d.exec_()
        
        def signSeed():
            errorFlag = False
            
            def getSeed():
                try:
                    seed = str(openFile("Open seed")).encode('utf-8')
                except:
                    errorFlag = True
                    errorDialog("No file chosen for opening")

            try:
                file = str(openFile()).encode('utf-8')
            except:
                errorFlag = True
                errorDialog("No file chosen for opening")
            if(not errorFlag):
                keys = RSA.generate(2048, getSeed())
                pubkey = keys.publickey()
                hash = SHA3_224.new(file)
                cipher = pss.new(keys).sign(hash)
                print(hash.hexdigest())
                print(cipher)
                try:
                    saveFileBin(cipher, "Save signature")
                except:
                    errorFlag = True
                    errorDialog("File saving aborted by user")
                keySTR = pubkey.export_key(format='PEM', passphrase=None, pkcs=1, protection=None, randfunc=None)

                def saveKey():
                    filename = QFileDialog.getSaveFileName(self, "Save key file", "", ".PEM")
                    try:
                        if not filename[0]: raise IOError("No file selected")
                        f = open(filename[0], 'wb')
                        f.write(keySTR)
                        f.close()
                    except:
                        errorFlag = True
                        errorDialog("File saving aborted by user")
            
            if(not errorFlag):
                d = QDialog()
                d.setWindowTitle("Done")
                d.resize(300, 340)
                txt = QTextEdit(d)
                txt.resize(280, 240)
                txt.move(10, 10)
                txt.setReadOnly(True)
                txt.setText("Here is your private key. KEEP IT SAFE!\n" + keySTR.decode("utf-8"))
                btn = QPushButton("Noted", d)
                btn.setToolTip('Make sure, I will not show it again')
                btn.resize(200, 30)
                btn.move(50, 260)
                btn.clicked.connect(d.accept)
                btn2 = QPushButton("Just save it", d)
                btn2.setToolTip('To file?')
                btn2.resize(200, 30)
                btn2.move(50, 300)
                btn2.clicked.connect(saveKey)
                d.exec_()

        def validate():
            errorFlag = False
            try:
                file = str(openFile()).encode('utf-8')
            except:
                errorFlag = True
                errorDialog("No file chosen for opening")
                return
            try:
                signature = openFileBin("Open signature file").read()
            except:
                errorFlag = True
                errorDialog("No file chosen for opening")
                return
            try:
                Key = RSA.import_key(openFileBin("Open key file").read())
            except:
                errorFlag = True
                errorDialog("No file chosen for opening")
                return
            if(not errorFlag):
                if(check(file, signature, Key)):
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

        buttonNewFile = QPushButton('Sign with random key', self)
        buttonNewFile.setToolTip('Sign new file')
        buttonNewFile.resize(200, 30)
        buttonNewFile.move(50, 20)
        buttonNewFile.clicked.connect(sign)

        buttonNewFile = QPushButton('Sign with key from seed', self)
        buttonNewFile.setToolTip('Sign new file with own key')
        buttonNewFile.resize(200, 30)
        buttonNewFile.move(50, 60)
        buttonNewFile.clicked.connect(signSeed)

        buttonOpenFile = QPushButton('Validate', self)
        buttonOpenFile.setToolTip('Validate file with existing signature')
        buttonOpenFile.resize(200, 30)
        buttonOpenFile.move(50, 100)
        buttonOpenFile.clicked.connect(validate)

        buttonExit = QPushButton('Exit', self)
        buttonExit.setToolTip('Do I need to explain this functionality?')
        buttonExit.resize(200, 30)
        buttonExit.move(50, 140)
        buttonExit.clicked.connect(self.close)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
