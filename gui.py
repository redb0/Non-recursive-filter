import sys
from PyQt5.QtWidgets import QApplication, QAction, qApp
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtWidgets import QSpinBox, QVBoxLayout, QTextEdit, QFormLayout, QPushButton

from PyQt5.QtGui import QIcon, QKeySequence

from sound import open_file, main

from document_manager import manager

from sin import main_sin
# import sin


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # добавление меню бара
        menubar = self.menuBar()
        # добавление пунктов меню
        fileMenu = menubar.addMenu('&File')

        # значек & перед одной из букв в названии менюшки
        # позволяет выбирать его по нажатии буквы на клавиатуре поле альта

        # меню "открыть файл"
        fileOpenAction = QAction('&Open file', self)
        # сочетание клавиш для этого действия
        # fileOpenAction.setShortcut(QKeySequence(self.tr('CTRL+F')))
        fileOpenAction.setShortcuts(QKeySequence.keyBindings(QKeySequence.Open))
        # пояснение в строке состояния
        fileOpenAction.setStatusTip('Открыть файл')
        # присоединение действия к сигналу
        fileOpenAction.triggered.connect(self.showOpenDialog)

        # меню выход из программы
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut(QKeySequence(self.tr('CTRL+Q')))
        # Windows не имеет сочетания клавишь для выхода
        # exitAction.setShortcuts(QKeySequence.keyBindings(QKeySequence.Quit))
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        # добавление в меню 'файл'
        fileMenu.addAction(fileOpenAction)
        fileMenu.addAction(exitAction)

        self.statusBar()

        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('BitCrusher')

        self.intervalSpin_N = QSpinBox(self)
        self.intervalSpin_N.setRange(1, 500)
        self.intervalSpin_N.setMaximum(500)
        self.intervalSpin_N.setValue(20)

        self.intervalSpin_Fs = QSpinBox(self)
        self.intervalSpin_Fs.setRange(1, 2000)
        self.intervalSpin_Fs.setMaximum(2000)
        self.intervalSpin_Fs.setValue(200)

        self.intervalSpin_Fx = QSpinBox(self)
        self.intervalSpin_Fx.setRange(1, 2000)
        self.intervalSpin_Fx.setMaximum(2000)
        self.intervalSpin_Fx.setValue(300)

        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)


        # кнопка
        self.resButton = QPushButton("Применить фильтр")
        # кнопка
        self.sinButton = QPushButton("Нужно больше (золота) наглядности")

        def sinButtonCilcked():
            # Порядок фильтра
            N = self.intervalSpin_N.value()
            Fs = self.intervalSpin_Fs.value()
            Fx = self.intervalSpin_Fx.value()

            self.textEdit.setText('True')

            # main_sin(N, Fs, Fx)

        def buttonCilcked():
            if manager.get_current():
                # Порядок фильтра
                N = self.intervalSpin_N.value()
                Fs = self.intervalSpin_Fs.value()
                Fx = self.intervalSpin_Fx.value()

                def myLogger(*args):
                    console = self.textEdit
                    for i in args:
                        console.append(str(i))

                if manager.get_current() != "":
                    (data, nchannels, sampwidth, framerate, nframes, comptype) = open_file(manager.get_current(), myLogger)
                    f_to_save_in_1 = self.showSaveDialog()
                    f_to_save_in_1 = f_to_save_in_1[0][:-4] + "_writeframesraw_" + f_to_save_in_1[0][-4:]
                    f_to_save_in_1 = open(f_to_save_in_1, 'wb')
                    main(data, nchannels, sampwidth, framerate, comptype, N, myLogger, f_to_save_in_1, Fs, Fx)
                    f_to_save_in_1.close()

        self.resButton.clicked.connect(buttonCilcked)
        self.sinButton.clicked.connect(sinButtonCilcked)

        # вуктикальное расположение виджетов
        vbox = QVBoxLayout()
        wdg = QWidget()
        self.setCentralWidget(wdg)

        # добавляет строку с парой виджет виджет или строка виджет
        form = QFormLayout()
        form.addRow("Порядок фильтра", self.intervalSpin_N)
        form.addRow("Частота полосы пропускания", self.intervalSpin_Fs)
        form.addRow("Частота полосы затухания", self.intervalSpin_Fx)
        # добавлять сюда
        vbox.addLayout(form)
        vbox.addWidget(self.textEdit)
        vbox.addWidget(self.resButton)
        vbox.addWidget(self.sinButton)

        wdg.setLayout(vbox)

        self.show()

    def showOpenDialog(self):
        manager.clear()
        file_name = QFileDialog.getOpenFileName(self, 'Открыть файл', '/', '*.wav')[0]
        if file_name != "":
            manager.add(file_name)
            self.textEdit.append("----------Файл загружен----------")

    def showSaveDialog(self):
        save_file_name = QFileDialog.getSaveFileName(self, "Сохранить как", manager.get_current() + "_NEW",
                                                     "Waveform Audio (*.wav)", options=QFileDialog.Options())

        if save_file_name != "":
            return save_file_name


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
