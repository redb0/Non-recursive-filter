import unittest

import sys
from unittest.mock import Mock

from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication

from gui import MainWindow
import sin


class MyTestCase(unittest.TestCase):
    def setUp(self):
        """Подготовка фикстуры"""

        # Требование QT - перед созданием виджета необходимо создать приложение.
        # Приложение создается однократно
        self.app = QApplication.instance() or QApplication(sys.argv)
        # Создаваемое окно не назначается главным окном приложения, т.к. приложение не будет запускаться
        self.w = MainWindow()

    def test_default_state(self):
        self.assertEqual(self.w.intervalSpin_N.value(), 20)
        self.assertEqual(self.w.intervalSpin_Fs.value(), 200)
        self.assertEqual(self.w.intervalSpin_Fx.value(), 300)
        self.assertEqual(self.w.textEdit.isReadOnly(), True)

    def test_incorrect_input1(self):
        QTest.keyClicks(self.w.intervalSpin_N, 'qwerty')
        QTest.keyClicks(self.w.intervalSpin_N, 'qwerty')
        QTest.keyClicks(self.w.intervalSpin_N, 'qwerty')
        self.assertTrue(self.w.intervalSpin_N.value(), 20)
        self.assertEqual(self.w.intervalSpin_Fs.value(), 200)
        self.assertEqual(self.w.intervalSpin_Fx.value(), 300)

    def test_incorrect_input2(self):
        QTest.keyClicks(self.w.intervalSpin_N, '0')
        QTest.keyClicks(self.w.intervalSpin_N, '0')
        QTest.keyClicks(self.w.intervalSpin_N, '0')
        self.assertTrue(self.w.intervalSpin_N.value(), 20)
        self.assertEqual(self.w.intervalSpin_Fs.value(), 200)
        self.assertEqual(self.w.intervalSpin_Fx.value(), 300)

    def test_incorrect_input3(self):
        QTest.keyClicks(self.w.intervalSpin_N, '501')
        QTest.keyClicks(self.w.intervalSpin_N, '2001')
        QTest.keyClicks(self.w.intervalSpin_N, '2001')
        self.assertTrue(self.w.intervalSpin_N.value(), 20)
        self.assertEqual(self.w.intervalSpin_Fs.value(), 200)
        self.assertEqual(self.w.intervalSpin_Fx.value(), 300)

    # @patch('main_sin')
    def test(self):

        sin.main_sin = Mock(return_value=self.w.textEdit.setText('True'))

        # self.w.sinButton.triggered.connect(lambda )
        QTest.mouseClick(self.w.sinButton, Qt.LeftButton)
        self.assertTrue(self.w.textEdit.toPlainText(), 'True') # self.w.textEdit.toPlainText()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
