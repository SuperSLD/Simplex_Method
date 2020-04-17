import sys
from fractions import Fraction

from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from linal.matrix import Matrix

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class GUI:
    """
    Главный класс в котором определяются
    параметры графического интерфейса.
    """

    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.app.setWindowIcon(QtGui.QIcon('icon200x200.png'))
        self.win = uic.loadUi("gaus.ui")

        self.A = []

        self.win.pushButton.clicked.connect(self.add_line)
        self.win.pushButton_2.clicked.connect(self.delete_all_lines)
        self.win.pushButton_3.clicked.connect(self.calculate_max)
        self.win.pushButton_4.clicked.connect(self.calculate_min)

        self.win.show()
        sys.exit(self.app.exec())
        return

    def add_line(self):
        """
        Добавление троки к матрице ограничений.
        """
        try:
            print("add_line")
            print(self.win.lineEdit.text())
            self.A.append([Fraction(a) for a in self.win.lineEdit.text().split(" ")])
            self.win.lineEdit.setText("")
            self.update_list_widget()
        except Exception as inst:
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)  # __str__ allows args to be printed directly
        return

    def delete_all_lines(self):
        """
        Отчистка матрицы ограничений.
        """
        print("delete_all_lines")
        self.A = []
        self.update_list_widget()
        return

    def update_list_widget(self):
        """
        Обновление информации в виджете
        с матрией рграничений.
        :return:
        """
        print("update_list_widget")
        self.win.listWidget_2.clear()
        print("clear ok")
        for i in range(len(self.A)):
            string = " + ".join([str(self.A[i][j])+"x"+str(j+1) for j in range(len(self.A[i])-1)])
            string += " <= " + str(self.A[i][len(self.A[i])-1])
            print(string)
            self.win.listWidget_2.addItem(string)
        return

    def calculate_min(self):
        """
        Поиск минимума.
        """
        self.data_preparation(False)
        return

    def calculate_max(self):
        """
        Поиск максимума.
        """
        self.data_preparation(True)
        return

    def data_preparation(self, max):
        """
        Подготовка данных для решения задачи.
        :param max: задача на максимум True.
        :return: вывод в список хода решения.
        """
        try:
            h = []
            C = [Fraction(self.win.lineEdit_3.text()) if max else -Fraction(self.win.lineEdit_3.text())]
            C += [-Fraction(a) if max else Fraction(a) for a in self.win.lineEdit_2.text().split(" ")]
            C += [0 for _ in range(len(self.A))]

            h.append(["SIMPLEX_TABLE create --> " + ("MAXIMUM" if max else "MINIMUM"), "#6DFFAA"])
            SIMPLEX_TABLE = [C]

            for i in range(len(self.A)):
                base = [self.A[i][len(self.A[i])-1]]
                base += [self.A[i][j] for j in range(len(self.A[i])-1)]
                base += [1 if i == j else 0 for j in range(len(self.A))]
                SIMPLEX_TABLE.append(base)

            Matrix.matrix_print(SIMPLEX_TABLE, h)
            v = Matrix.simplex_method(SIMPLEX_TABLE, h)
            h = v[0]
            h.append(["_"*50, "#FFFD91"])
            h.append(["simplex method end work", "#FFFFFF"])
            h.append(["optimal value: " + str(SIMPLEX_TABLE[0][0]), "#FF7F7F"])
            c = 1
            colors = ["#FF7F7F", "#FFB27F", "#FFE97F", "#A5FF7F", "#7FC9FF", "#7F92FF", "#D67FFF"]
            for x in v[1]:
                h.append(["X"+str(x)+" = " + str(SIMPLEX_TABLE[c][0]), colors[c % 7]])
                c += 1
            print("simplex method end work")
            self.win.listWidget.clear()
            for string in h:
                item= QtWidgets.QListWidgetItem(string[0])
                font = QtGui.QFont()
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                item.setForeground(QtGui.QColor(string[1]))
                self.win.listWidget.addItem(item)

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
        return


gui = GUI()
