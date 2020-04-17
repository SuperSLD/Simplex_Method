import copy
import sys
from fractions import Fraction


class Matrix:
    """
    Класс для операций над матрицей.
    """

    @staticmethod
    def gaus(matrix, p=[[i, i] for i in range(100)]):
        """
        Метод Гауса-Жордана.
        :param matrix: исходная матрица.
        :param p: координаты каждого разрешающего элемента.
        :return: список строк для вывода подробной информации.
        """
        h = []
        n = len(matrix)
        Matrix.matrix_print(matrix, h)
        for k in range(n):
            Matrix.one_replace(matrix, p[k][0], p[k][1])
            Matrix.matrix_print(matrix, h)
        return h

    @staticmethod
    def one_replace(matrix, x, y):
        """
        Итерация однократного замещения
        :param matrix: исходная матрица.
        :param x: строка
        :param y: столбец
        """
        key = copy.copy(matrix[y])
        n = len(matrix)
        if key[x] == 0: return []
        for j in range(n):
            key2 = matrix[j][x]
            for i in range(len(matrix[j])):
                matrix[j][i] = matrix[j][i] / key[x] if y == j else matrix[j][i] - key2 * key[i] / key[x]
        return

    @staticmethod
    def matrix_print(matrix, h):
        """
        Сохранение информации о действии над матрицей
        дл последующего вывода.
        :param matrix: матрица
        :param h: список для записи информации.
        """
        print("-" * 40)
        h.append(["-"*40, "#FFFD91"])
        SYMBOL_SIZE = 7
        if len(matrix) != 0:
            for i in range(len(matrix)):
                print("".join([str(f)+" "*(SYMBOL_SIZE-len(str(f))) for f in matrix[i]]))
                h.append(["".join([" "*(SYMBOL_SIZE-len(str(f))) + str(f) for f in matrix[i]]), "#75FFF1"])
        else:
            print("Решений нет")
            h.append(["Решений нет", "#6DFFAA"])
        return

    @staticmethod
    def simplex_method(SIMPLEX_TABLE, h):
        """
        Симплекс метод решения задачи линейного програмирования.
        :param SIMPLEX_TABLE: симплекс таблица составленная из условий.
        :return: информация об проделанных операциях.
        """
        info = [True, 0, 0]
        number_base = [len(SIMPLEX_TABLE[0])-len(SIMPLEX_TABLE)+i+1 for i in range(len(SIMPLEX_TABLE) - 1)]
        iteration_count = 0
        while info[0]:
            iteration_count += 1
            info = Matrix.__check_vector(SIMPLEX_TABLE[0])
            if not info[0]:
                break
            h.append(["_"*50, "#6DFFAA"])
            h.append(["iteration " + str(iteration_count), "#FFBCA0"])
            h.append(["info : " + str(info[0]) + "; " + str(info[1]) + "; " + str(info[2]), "#FFBCA0"])
            min = 10 ** 100
            index = -1
            for i in range(1, len(SIMPLEX_TABLE)):
                if SIMPLEX_TABLE[i][info[1]] > 0:
                    c = SIMPLEX_TABLE[i][0]/SIMPLEX_TABLE[i][info[1]]
                    if c < min:
                        min = c
                        index = i
            if index == -1:
                h.append(["the task is unsolvable", "#FF0000"])
                return h
            number_base[index-1] = info[1]
            h.append(["base param [" + str(info[1]) + ";" + str(index) + "]", "#FFBCA0"])
            Matrix.one_replace(SIMPLEX_TABLE, info[1], index)
            Matrix.matrix_print(SIMPLEX_TABLE, h)
            h.append(["\nX -> " + " ".join([str(a) for a in number_base]), "#A7FF7F"])

        return [h, number_base]

    @staticmethod
    def __check_vector(C):
        """
        (Вспомогательная функция для simplex_method)
        Проверка вектора С на наличие
        значения удоволетворяющего условиям.
        :param C:
        :return:
        """
        info = [False, 0, 0]
        min = 10**100
        for i in range(1, len(C)):
            if C[i] < 0 and C[i] < min:
                min = C[i]
                info[0] = True
                info[1] = i
                info[2] = min
        print("info : " + str(info[0]) + "; " + str(info[1]) + "; " + str(info[2]))
        return info

