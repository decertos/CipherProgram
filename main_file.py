import sys
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication
from itertools import cycle
from PyQt6 import uic
import sqlite3
from os.path import isfile
import pyperclip


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/main_window.ui", self)
        self.atbash.clicked.connect(self.atbash_open)
        self.caesar.clicked.connect(self.caesar_open)
        self.vizhener.clicked.connect(self.vizhener_open)
        self.vizhener_key.clicked.connect(self.vizhener_decrypt_open)
        self.polibium.clicked.connect(self.polibium_open)
        self.alphabets.clicked.connect(self.alphabets_open)

        created = True
        if not isfile("alphabets.db"):
            created = False
        conn = sqlite3.connect("alphabets.db")
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Alphabets (title TEXT UNIQUE, alphabet TEXT)""")
        conn.commit()
        if not created:
            examples = {"русский": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                        "русский (без ё)": "абвгдежзийклмнопрстуфхцчшщъыьэюя",
                        "английский": "abcdefghijklmnopqrstuvwxyz",
                        "доска Полибия (русский без ё)": "абвгдежз\nийклмноп\nрстуфхцч\nшщъыьэюя",
                        "доска Полибия (английский)": "abcdef\nghijkl\nmnopqr\nstuvwx\nyz    "}
            for i in examples:
                cur.execute("""INSERT INTO Alphabets (title, alphabet) VALUES (?, ?)""", (i, examples[i]))
                conn.commit()
        cur.close()
        conn.close()

    def atbash_open(self):
        self.atbashWindow = Atbash()
        self.atbashWindow.show()

    def caesar_open(self):
        self.caesarWindow = Caesar()
        self.caesarWindow.show()

    def vizhener_open(self):
        self.vizhenerWindow = Vizhener()
        self.vizhenerWindow.show()

    def vizhener_decrypt_open(self):
        self.vizhenerDecryptWindow = VizhenerDecrypt()
        self.vizhenerDecryptWindow.show()

    def polibium_open(self):
        self.polibiumWindow = PolibiumBoard()
        self.polibiumWindow.show()

    def alphabets_open(self):
        self.alphabetsWindow = AlphabetsMenu()
        self.alphabetsWindow.show()


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


class VizhenerDecrypt(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/vizhener_decrypt.ui", self)

        self.get_key_button.clicked.connect(self.get_key)

    def get_key(self):
        plain_text = self.deciphered.toPlainText()
        ciphered = self.ciphered.toPlainText()
        alphabet = self.alphabet.text()
        from_indexes_lower = {i: alphabet[i].lower() for i in range(len(alphabet))}
        to_indexes_lower = {alphabet[i].lower(): i for i in range(len(alphabet))}

        self.infoLabel.setText("")

        if len(ciphered) != len(plain_text):
            self.infoLabel.setText("Длины текстов\nне совпадают")
            return

        for i in range(len(plain_text)):
            if to_indexes_lower.get(plain_text[i].lower(), None) is None:
                self.infoLabel.setText("Есть символы\nне из алфавита")
                break
            elif to_indexes_lower.get(ciphered[i].lower(), None) is None:
                self.infoLabel.setText("Есть символы\nне из алфавита")
                break

        ROT = int(self.rot1.isChecked())
        key = ""

        for i in range(len(plain_text)):
            if to_indexes_lower.get(plain_text[i].lower(), None) is None:
                continue
            if to_indexes_lower.get(ciphered[i].lower(), None) is None:
                continue
            plain_text_index = to_indexes_lower[plain_text[i].lower()]
            ciphered_index = to_indexes_lower[ciphered[i].lower()]
            key_symbol = (ciphered_index - plain_text_index - ROT) % len(alphabet)
            key += from_indexes_lower[key_symbol]

        self.key.setPlainText(key)


class PolibiumBoard(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/polibium_board.ui", self)
        self.cipher_button.clicked.connect(self.cipher)
        self.decipher_button.clicked.connect(self.decipher)

        board = []
        length = -1
        x_length, y_length = 0, 0
        for i in self.board.toPlainText().split("\n"):
            board.append(i.strip("\n"))
            if length == -1:
                length = len(board[-1])
                x_length = length
            else:
                if length != len(board[-1]):
                    self.infoLabel.setText("Длины строк\nне совпадают")
                    return
        y_length = len(board)

        self.cipher_value.setMaximum(y_length)

    def cipher(self):
        board = []
        length = -1
        self.infoLabel.setText("")
        all_symbols = set()

        x_length, y_length = 0, 0
        for i in self.board.toPlainText().split("\n"):
            board.append(i.strip("\n"))
            for j in board[-1]:
                set_length = len(all_symbols)
                all_symbols.add(j)
                if set_length == len(all_symbols):
                    self.infoLabel.setText("Символы доски\nне уникальные")
                    return
            if length == -1:
                length = len(board[-1])
                x_length = length
            else:
                if length != len(board[-1]):
                    self.infoLabel.setText("Длины строк\nне совпадают")
                    return
        y_length = len(board)

        self.cipher_value.setMaximum(y_length)

        text = self.deciphered.toPlainText()
        from_indexes_lower = {}
        to_indexes_lower = {}
        for i in range(len(board)):
            for j in range(len(board[i])):
                from_indexes_lower[(i, j)] = board[i][j]
                to_indexes_lower[board[i][j]] = (i, j)

        dx, dy, length = 0, 0, self.cipher_value.value()
        values = {"вверх": (0, -1), "вправо": (1, 0),
                  "вниз": (0, 1), "влево": (-1, 0)}
        dx, dy = values[self.cipher_direction.currentText()]
        dx, dy = dx * length, dy * length
        ciphered_text = ""
        for symbol in text:
            if to_indexes_lower.get(symbol.lower(), None) is None:
                self.infoLabel.setText("В тексте есть\nсимволы не\nиз доски")
                ciphered_text += symbol
                continue
            symbol_index = to_indexes_lower[symbol.lower()]
            new_symbol_index = ((symbol_index[0] + dy) % y_length, (symbol_index[1] + dx) % x_length)
            ciphered_text += from_indexes_lower[new_symbol_index].lower() if symbol.islower() \
                else from_indexes_lower[new_symbol_index].upper()

        self.ciphered.setPlainText(ciphered_text)

    def decipher(self):
        board = []
        length = -1
        self.infoLabel.setText("")
        all_symbols = set()

        x_length, y_length = 0, 0
        for i in self.board.toPlainText().split("\n"):
            board.append(i.strip("\n"))
            for j in board[-1]:
                set_length = len(all_symbols)
                all_symbols.add(j)
                if set_length == len(all_symbols):
                    self.infoLabel.setText("Символы доски\nне уникальные")
                    return
            if length == -1:
                length = len(board[-1])
                x_length = length
            else:
                if length != len(board[-1]):
                    self.infoLabel.setText("Длины строк\nне совпадают")
                    return
        y_length = len(board)

        self.cipher_value.setMaximum(y_length)

        text = self.ciphered.toPlainText()
        from_indexes_lower = {}
        to_indexes_lower = {}
        for i in range(len(board)):
            for j in range(len(board[i])):
                from_indexes_lower[(i, j)] = board[i][j]
                to_indexes_lower[board[i][j]] = (i, j)

        dx, dy, length = 0, 0, self.cipher_value.value()
        values = {"вверх": (0, -1), "вправо": (1, 0),
                  "вниз": (0, 1), "влево": (-1, 0)}
        dx, dy = values[self.cipher_direction.currentText()]
        dx, dy = -dx * length, -dy * length
        deciphered_text = ""
        for symbol in text:
            if to_indexes_lower.get(symbol.lower(), None) is None:
                self.infoLabel.setText("В тексте есть\nсимволы не\nиз доски")
                deciphered_text += symbol
                continue
            symbol_index = to_indexes_lower[symbol.lower()]
            new_symbol_index = ((symbol_index[0] + dy) % y_length, (symbol_index[1] + dx) % x_length)
            deciphered_text += from_indexes_lower[new_symbol_index].lower() if symbol.islower() \
                else from_indexes_lower[new_symbol_index].upper()

        self.deciphered.setPlainText(deciphered_text)


class AlphabetsMenu(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/alphabets.ui", self)
        self.update_list()

        self.copy_button.clicked.connect(self.copy_alphabet)
        self.create_button.clicked.connect(self.add_alphabet)
        self.delete_button.clicked.connect(self.delete_alphabet)

        self.alphabetSelect.currentTextChanged.connect(self.set_alphabet)

    def set_alphabet(self):
        current_alphabet = self.alphabetSelect.currentText()
        if not current_alphabet:
            return
        self.alphabet.setPlainText(self.alphabets[current_alphabet])
        self.length.setText(f"Длина: {len(self.alphabets[current_alphabet])}")

    def copy_alphabet(self):
        alphabet = self.alphabet.toPlainText()
        pyperclip.copy(alphabet)

    def update_list(self):
        self.alphabetSelect.clear()
        self.alphabets = []
        conn = sqlite3.connect("alphabets.db")
        cur = conn.cursor()
        all_data = cur.execute("""SELECT * FROM Alphabets""").fetchall()
        self.alphabets = {}
        for i in all_data:
            self.alphabets[i[0]] = i[1]
        cur.close()
        conn.close()
        first_alphabet = None
        for i in self.alphabets:
            if first_alphabet is None:
                first_alphabet = self.alphabets[i]
            title = i
            self.alphabetSelect.addItem(title)

        if self.alphabets:
            self.alphabet.setPlainText(first_alphabet)
            self.length.setText(f"Длина: {len(first_alphabet)}")
        else:
            self.length.setText("Нет длины")

    def add_alphabet(self):
        self.addAlphabetWindow = AddAlphabet(self)
        self.addAlphabetWindow.show()

    def delete_alphabet(self):
        self.deleteAlphabetWindow = DeleteAlphabet(self)
        self.deleteAlphabetWindow.show()


class AddAlphabet(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("uis/create_alphabet.ui", self)
        self.window_parent = parent
        self.create_button.clicked.connect(self.add_alphabet)
        self.cancel_button.clicked.connect(self.cancel_creating)

    def add_alphabet(self):
        title, alphabet = self.title.text(), self.alphabet.toPlainText()
        self.infoLabel.setText("")
        for i in self.window_parent.alphabets:
            if i == title:
                self.infoLabel.setText("Алфавит с\nтаким названием\nуже существует")
                return
        if not title or not alphabet:
            self.infoLabel.setText("Заполните все поля")
            return
        conn = sqlite3.connect("alphabets.db")
        cur = conn.cursor()
        cur.execute("""INSERT INTO Alphabets (title, alphabet) VALUES (?, ?)""", (title, alphabet))
        conn.commit()
        cur.close()
        conn.close()
        self.window_parent.update_list()
        self.close()

    def cancel_creating(self):
        self.close()


class DeleteAlphabet(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("uis/delete_alphabet.ui", self)
        self.window_parent = parent
        for i in parent.alphabets:
            self.alphabetSelect.addItem(i)
        self.delete_button.clicked.connect(self.delete_alphabet)
        self.cancel_button.clicked.connect(self.cancel_adding)

    def delete_alphabet(self):
        title = self.alphabetSelect.currentText()
        if not title:
            self.infoLabel.setText("Не выбран алфавит")
            return
        conn = sqlite3.connect("alphabets.db")
        cur = conn.cursor()
        cur.execute("""DELETE FROM Alphabets WHERE title = ?""", (title, ))
        conn.commit()
        cur.close()
        conn.close()
        self.window_parent.update_list()
        self.close()

    def cancel_adding(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())