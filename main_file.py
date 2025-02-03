import sys
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication
from itertools import cycle
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/main_window.ui", self)
        self.atbash.clicked.connect(self.atbash_open)
        self.caesar.clicked.connect(self.caesar_open)
        self.vizhener.clicked.connect(self.vizhener_open)

    def atbash_open(self):
        self.atbashWindow = Atbash()
        self.atbashWindow.show()

    def caesar_open(self):
        self.caesarWindow = Caesar()
        self.caesarWindow.show()

    def vizhener_open(self):
        self.vizhenerWindow = Vizhener()
        self.vizhenerWindow.show()


class Atbash(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/atbash.ui", self)
        self.cipher_button.clicked.connect(self.cipher)
        self.decipher_button.clicked.connect(self.decipher)

    def cipher(self):
        text = self.deciphered.toPlainText()
        alphabet = self.alphabet.text()

        from_indexes_lower = {i: alphabet[i].lower() for i in range(len(alphabet))}
        to_indexes_lower = {alphabet[i].lower(): i for i in range(len(alphabet))}
        from_indexes_upper = {i: alphabet[i].upper() for i in range(len(alphabet))}
        to_indexes_upper = {alphabet[i].upper(): i for i in range(len(alphabet))}

        ciphered_text = ""
        for symbol in text:
            if to_indexes_lower.get(symbol.lower(), None) is None:
                ciphered_text += symbol
                continue
            symbol_index = to_indexes_lower[symbol] if symbol.islower() else to_indexes_upper[symbol]
            new_index = len(alphabet) - symbol_index - 1
            ciphered_text += from_indexes_lower[new_index] if symbol.islower() \
                else from_indexes_upper[new_index]
        self.ciphered.setPlainText(ciphered_text)

    def decipher(self):
        text = self.ciphered.toPlainText()
        alphabet = self.alphabet.text()

        from_indexes_lower = {i: alphabet[i].lower() for i in range(len(alphabet))}
        to_indexes_lower = {alphabet[i].lower(): i for i in range(len(alphabet))}
        from_indexes_upper = {i: alphabet[i].upper() for i in range(len(alphabet))}
        to_indexes_upper = {alphabet[i].upper(): i for i in range(len(alphabet))}

        deciphered_text = ""
        for symbol in text:
            if to_indexes_lower.get(symbol.lower(), None) is None:
                deciphered_text += symbol
                continue
            symbol_index = to_indexes_lower[symbol] if symbol.islower() else to_indexes_upper[symbol]
            new_index = len(alphabet) - symbol_index - 1
            deciphered_text += from_indexes_lower[new_index] if symbol.islower() \
                else from_indexes_upper[new_index]
        self.deciphered.setPlainText(deciphered_text)


class Caesar(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/caesar.ui", self)

        self.cipher_button.clicked.connect(self.cipher)
        self.decipher_button.clicked.connect(self.decipher)
        self.alphabet.textChanged.connect(self.textChanged)
        self.textChanged()

    def cipher(self):
        text = self.deciphered.toPlainText()
        alphabet = self.alphabet.text()
        shift = self.shift.value()

        from_indexes_lower = {i: alphabet[i].lower() for i in range(len(alphabet))}
        to_indexes_lower = {alphabet[i].lower(): i for i in range(len(alphabet))}
        from_indexes_upper = {i: alphabet[i].upper() for i in range(len(alphabet))}
        to_indexes_upper = {alphabet[i].upper(): i for i in range(len(alphabet))}

        ciphered_text = ""
        for symbol in text:
            if to_indexes_lower.get(symbol.lower(), None) is None:
                ciphered_text += symbol
                continue
            symbol_index = to_indexes_lower[symbol] if symbol.islower() else to_indexes_upper[symbol]
            new_index = (symbol_index + shift) % len(alphabet)
            ciphered_text += from_indexes_lower[new_index] if symbol.islower() \
                else from_indexes_upper[new_index]
        self.ciphered.setPlainText(ciphered_text)

    def decipher(self):
        text = self.ciphered.toPlainText()
        alphabet = self.alphabet.text()
        shift = self.shift.value()

        from_indexes_lower = {i: alphabet[i].lower() for i in range(len(alphabet))}
        to_indexes_lower = {alphabet[i].lower(): i for i in range(len(alphabet))}
        from_indexes_upper = {i: alphabet[i].upper() for i in range(len(alphabet))}
        to_indexes_upper = {alphabet[i].upper(): i for i in range(len(alphabet))}

        deciphered_text = ""
        for symbol in text:
            if to_indexes_lower.get(symbol.lower(), None) is None:
                deciphered_text += symbol
                continue
            symbol_index = to_indexes_lower[symbol] if symbol.islower() else to_indexes_upper[symbol]
            new_index = (symbol_index - shift) % len(alphabet)
            deciphered_text += from_indexes_lower[new_index] if symbol.islower() \
                else from_indexes_upper[new_index]
        self.deciphered.setPlainText(deciphered_text)

    def textChanged(self):
        self.shift.setMaximum(len(self.alphabet.text()))
        self.shift.setMinimum(-len(self.alphabet.text()))


class Vizhener(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/vizhener.ui", self)

        self.cipher_button.clicked.connect(self.cipher)
        self.decipher_button.clicked.connect(self.decipher)

    def cipher(self):
        text = self.deciphered.toPlainText()
        alphabet = self.alphabet.text()
        from_indexes_lower = {i: alphabet[i].lower() for i in range(len(alphabet))}
        to_indexes_lower = {alphabet[i].lower(): i for i in range(len(alphabet))}

        self.infoLabel.setText("")

        ROT = int(self.rot1.isChecked())

        if not self.key.text():
            self.infoLabel.setText("Ключ не должен\nбыть пустым")
            return

        for symbol in self.key.text():
            if to_indexes_lower.get(symbol.lower(), None) is None:
                self.infoLabel.setText("Ключ не полностью\nсостоит из\nсимволов алфавита")
                return

        key = cycle(self.key.text())

        ciphered_text = ""

        for symbol in text:
            if to_indexes_lower.get(symbol.lower(), None) is None:
                self.infoLabel.setText("Некоторых\nсимволов не было\nв алфавите,\nони не были\nзаменены.")
                ciphered_text += symbol
                continue
            key_symbol = next(key)
            text_symbol_index = to_indexes_lower[symbol.lower()]
            key_symbol_index = to_indexes_lower[key_symbol.lower()]
            new_symbol_index = (text_symbol_index + ROT + key_symbol_index) % len(alphabet)
            ciphered_text += from_indexes_lower[new_symbol_index].lower() if symbol.islower() else (
                from_indexes_lower[new_symbol_index].upper())

        self.ciphered.setPlainText(ciphered_text)

    def decipher(self):
        text = self.ciphered.toPlainText()
        alphabet = self.alphabet.text()
        from_indexes_lower = {i: alphabet[i].lower() for i in range(len(alphabet))}
        to_indexes_lower = {alphabet[i].lower(): i for i in range(len(alphabet))}

        self.infoLabel.setText("")

        ROT = int(self.rot1.isChecked())

        if not self.key.text():
            self.infoLabel.setText("Ключ не должен\nбыть пустым")
            return

        for symbol in self.key.text():
            if to_indexes_lower.get(symbol.lower(), None) is None:
                self.infoLabel.setText("Ключ не полностью\nсостоит из\nсимволов алфавита")
                return

        deciphered_text = ""
        key = cycle(self.key.text())

        for symbol in text:
            if to_indexes_lower.get(symbol.lower(), None) is None:
                self.infoLabel.setText("Некоторых\nсимволов не было\nв алфавите,\nони не были\nзаменены.")
                deciphered_text += symbol
                continue
            key_symbol = next(key)
            text_symbol_index = to_indexes_lower[symbol.lower()]
            key_symbol_index = to_indexes_lower[key_symbol.lower()]
            new_symbol_index = (text_symbol_index - key_symbol_index - ROT) % len(alphabet)
            deciphered_text += from_indexes_lower[new_symbol_index].lower() if symbol.islower() \
                else from_indexes_lower[new_symbol_index].upper()

        self.deciphered.setPlainText(deciphered_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())