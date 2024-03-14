import sqlite3
import sys
from random import randint

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


FINALCOUNTDOWN = 11
limit_hints = 3
limit_words = 10


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("ui-files/game_window.ui", self)
        self.setFixedSize(900, 750)
        self.db = sqlite3.connect("abc.sqlite")
        self.btn_exit.clicked.connect(self.back_menu)
        self.lamp_btn.clicked.connect(self.hint)

        self.correct_letters = []
        self.incorrect_letters = []
        self.limit_number_hint = 0
        self.limit_number_word = 0
        self.true_answer = 0
        self.false_answer = 0

        self.create_keyboard()

        self.choise_word()
        self.translate_word()

    def create_keyboard(self):
        keyboardlayout = QGridLayout()
        self.grandlayout.addLayout(keyboardlayout)
        buttons = [
            'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё',
            'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М',
            'Н', 'О', 'П', 'Р', 'С', 'Т', 'У',
            'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ',
            'Ы', 'Ь', 'Э', 'Ю', 'Я', '-', ' '
        ]

        row = 0
        col = 0
        for button in buttons:
            btn = QPushButton(button)
            btn.clicked.connect(self.checking)
            keyboardlayout.addWidget(btn, row, col)
            col += 1
            if col > 8:
                col = 0
                row += 1

        self.setLayout(self.grandlayout)
        self.show()

    def checking(self):
        sender = self.sender()
        text = sender.text()
    
        wordlist = list(self.word)

        if text.lower() in wordlist and not(text.lower() in self.correct_letters):
            self.correct_letters.append(text.lower())
            for i in range(len(wordlist)):
                if text.lower() == wordlist[i]:
                    self.coding_word[i] = text
        else:
            self.incorrect_letters.append(text.lower())
            self.imagine_picture()

        self.label.setText(''.join(self.coding_word))
        self.imagine_picture()
        self.final_moved()

    def final_moved(self):
        if len(self.incorrect_letters) == FINALCOUNTDOWN or len(set(self.correct_letters)) == len(set(list(self.word))):
            self.image_final_pict()
            self.zeroing_lists()
            if self.limit_number_word < limit_words:
                self.imagine_picture()
                self.choise_word()
                self.translate_word()
            else:
                self.game_over()

    def game_over(self):
        self.final_window = FinalGame(self.true_answer, self.false_answer)
        self.back_menu()
        self.final_window.show()
        self.close()

    def hint(self):
        if self.limit_number_hint < limit_hints:
            self.limit_number_hint += 1
            for i in range(len(self.word)):
                    if not(self.word[i] in self.correct_letters):
                        self.correct_letters.append(self.word[i])
                        for j in range(len(self.word)):
                            if self.word[i] == self.word[j]:
                                self.coding_word[j] = self.word[i]
                        break

        self.label.setText(''.join(self.coding_word))
        
        self.final_moved()

    def image_final_pict(self):
        if len(self.incorrect_letters) == FINALCOUNTDOWN:
            self.window = AnswerF(self.word)
            self.false_answer += 1
        else:
            self.window = AnswerT(self.word)
            self.true_answer += 1
        self.window.show()

    def choise_word(self):
        self.limit_number_word += 1
        cursor = self.db.cursor()

        random_number = self.random_number()
        cursor.execute('SELECT word FROM nouns WHERE rowid = ?', (random_number,))
        result = cursor.fetchall()[0][0]

        self.word = result
        return self.word

    def random_number(self):
        cursor = self.db.cursor()

        cursor.execute('SELECT Count(*) FROM nouns')
        summar = cursor.fetchall()[0][0]
        number = randint(1, summar + 1)

        return number

    def translate_word(self):
        word = self.word
        self.coding_word = list('_' * len(word))
        self.label.setText(''.join(self.coding_word))

    def imagine_picture(self):
        number = len(self.incorrect_letters)

        pixmap = QPixmap(f'pict/{number}.png')
        self.central_label.setPixmap(pixmap)

    def zeroing_lists(self):
        self.correct_letters = []
        self.incorrect_letters = []
        self.limit_number_hint = 0

    def back_menu(self):
        self.menu_window = Menu()
        self.menu_window.show()
        self.close()


class FinalGame(QDialog):
    def __init__(self, true_cnt_answers, false_cnt_answers):
        super().__init__()

        self.initUI(true_cnt_answers, false_cnt_answers)

    def initUI(self, t, f):
        uic.loadUi("ui-files/final_game_window.ui", self)

        pixmap_t = QPixmap('pict/True.png')
        pixmap_f = QPixmap('pict/False.png')

        self.true_label.setPixmap(pixmap_t)
        self.false_label.setPixmap(pixmap_f)

        self.true_count.setText(str(t))
        self.false_count.setText(str(f))


class AnswerT(QDialog):
    def __init__(self, word):
        super().__init__()

        self.initUI(word)

    def initUI(self, word):
        uic.loadUi("ui-files/answer_window.ui", self)

        pixmap = QPixmap('pict/win.png')
        self.pict_label.setPixmap(pixmap)

        self.text_label.setText(word)


class AnswerF(QDialog):
    def __init__(self, word):
        super().__init__()

        self.initUI(word)

    def initUI(self, word):
        uic.loadUi("ui-files/answer_window.ui", self)

        pixmap = QPixmap('pict/loose.png')
        self.pict_label.setPixmap(pixmap)

        self.text_label.setText(word)


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
    
        self.initUI()

    def initUI(self):
        self.show()
        uic.loadUi("ui-files/menu_window.ui", self)
        self.setFixedSize(800, 600)

        self.draw_menu()

        self.play_btn.clicked.connect(self.open_game)
        self.settings_btn.clicked.connect(self.open_settings)
        self.about_btn.clicked.connect(self.open_about)

    def draw_menu(self):
        pixmap = QPixmap('pict/menu_label.png')
        self.menu_label.setPixmap(pixmap)

    def open_game(self):
        self.game_window = Game()
        self.game_window.show()
        self.close()
    
    def open_settings(self):
        self.settings_window = Settings()
        self.settings_window.show()

    def open_about(self):
        self.about_window = About()
        self.about_window.show()


class Settings(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("ui-files/settings_window.ui", self)
        self.ok_btn.clicked.connect(self.save_settings)

    def save_settings(self):
        global limit_hints, limit_words, max_long_word
        limit_hints = self.number_hints.value()
        limit_words = self.limit_word.value()
        self.close()


class About(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("ui-files/about_window.ui", self)
        self.setFixedSize(400, 400)

        pixmap = QPixmap('pict/about.png')
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec())
