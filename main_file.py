import sys
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/main_window.ui", self)
        self.atbash.clicked.connect(self.atbash_open)

    def atbash_open(self):
        self.atbashWindow = Atbash()
        self.atbashWindow.show()


class Atbash(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/atbash.ui", self)
        self.cipher_button.clicked.connect(self.cipher)
        self.decipher_button.clicked.connect(self.decipher)

    def cipher(self):
        text = self.deciphered.toPlainText()
        alphabet = self.alphabet.text()
        from_indexes = {i: alphabet[i] for i in range(len(alphabet))}
        to_indexes = {alphabet[i]: i for i in range(len(alphabet))}

        ciphered_text = ""
        for symbol in text:
            if to_indexes.get(symbol, None) is None:
                ciphered_text += symbol
                continue
            symbol_index = to_indexes[symbol]
            ciphered_text += from_indexes[len(alphabet) - symbol_index - 1]
        self.ciphered.setPlainText(ciphered_text)

    def decipher(self):
        text = self.ciphered.toPlainText()
        alphabet = self.alphabet.text()
        from_indexes = {i: alphabet[i] for i in range(len(alphabet))}
        to_indexes = {alphabet[i]: i for i in range(len(alphabet))}

        deciphered_text = ""
        for symbol in text:
            if to_indexes.get(symbol, None) is None:
                deciphered_text += symbol
                continue
            symbol_index = to_indexes[symbol]
            deciphered_text += from_indexes[len(alphabet) - symbol_index - 1]
        self.deciphered.setPlainText(deciphered_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())