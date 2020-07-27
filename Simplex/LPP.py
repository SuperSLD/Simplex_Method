import copy
from fractions import Fraction


class LPP:
    def __init__(self):
        self.__W = []
        self.__A = []
        self.__optimal_value = None
        self.__optimal_table = None

    def add_W(self, W):
        """
        Добаляяем целевую функцию.
        :param W: массив коэффициентов.
        """
        for w in W:
            self.__W.append(Fraction(w))

    def add_limit(self, array):
        """
        Добавляем ограничения.
        :param array:
        :return:
        """
        a = []
        for elem in array:
            a.append(Fraction(elem))
        self.__A.append(a)

    def get_optimal_value(self):
        return self.__optimal_value

    def get_optimal_table(self):
        return self.__optimal_table

    def get_next_vector(self, p, length):
        """
        Получение следующего набора базисных переменных.
        :param p: базисные переменные.
        :param length: количество переменных
        :return: следующий набор.
        """
        check = False
        while not check:
            p[0][0] +=1
            for i in range(len(p)):
                if p[i][0] >= length:
                    p[i][0] -= length
                    p[i+1][0] += 1
            v = []
            check = True
            for i in range(len(p)): v.append(p[i][0]);
            for i in range(len(v)):
                try:
                    if v.index(v[i]) != i and v.index(v[i]) >= 0:
                        check = False
                except Exception as ex:
                    check = True
        return p

    def find_start_plan(self):
        """
        Поиск опорного базисного решения.
        """
        is_correct = False
        p = [[i, i] for i in range(len(self.__A))]
        p[0][0] -= 1
        while not is_correct:
            p = self.get_next_vector(p, len(self.__A[0]))
            clone_A = copy.copy(self.__A)

            is_correct = self.gaus(clone_A, p)
            for i in range(len(clone_A)):
                if clone_A[i][len(clone_A[i])-1] < 0:
                    is_correct = False

        start_plan = copy.copy(self.__A)
        self.gaus(start_plan, p)
        #self.matrix_print(start_plan)

        SIMPLEX_TABLE = []

        key_w = []
        for i in range(len(start_plan)):
            key_w.append(self.__W[p[i][0]])

        W0 = Fraction("0")
        for i in range(len(start_plan)):
            W0 += key_w[i] * start_plan[i][len(start_plan[0])-1]

        D_list = []
        for i in range(len(start_plan[0])-1):
            d = Fraction("0")
            for j in range(len(start_plan)):
                d += key_w[j]*start_plan[j][i]
            d -= self.__W[i]
            D_list.append(d)

        first_string = [W0]
        first_string.extend(D_list)
        SIMPLEX_TABLE.append(first_string)

        for matrix_string in start_plan:
            simplex_table_string = [matrix_string[len(matrix_string) - 1]]
            simplex_table_string.extend(matrix_string[:-1])
            SIMPLEX_TABLE.append(simplex_table_string)

        return SIMPLEX_TABLE

    def clear(self):
        """
        Отчистка параметров.
        :return:
        """
        self.__W = []
        self.__A = []
        self.__optimal_value = None
        self.__optimal_table = None

    def gaus(self, matrix, p=[[i, i] for i in range(100)]):
        """
        Метод Гауса-Жордана.
        :param matrix: исходная матрица.
        :param p: координаты каждого разрешающего элемента.
        :return: список строк для вывода подробной информации.
        """
        n = len(matrix)
        for k in range(n):
            if not self.one_replace(matrix, p[k][0], p[k][1]):
                return False
        return True

    def one_replace(self, matrix, x, y):
        """
        Итерация однократного замещения
        :param matrix: исходная матрица.
        :param x: строка
        :param y: столбец
        """
        key = copy.copy(matrix[y])
        n = len(matrix)
        if key[x] == 0: return False
        for j in range(n):
            key2 = matrix[j][x]
            for i in range(len(matrix[j])):
                matrix[j][i] = matrix[j][i] / key[x] if y == j else matrix[j][i] - key2 * key[i] / key[x]
        return True

    def matrix_print(self, matrix):
        """
        Сохранение информации о действии над матрицей
        дл последующего вывода.
        :param matrix: матрица
        :param h: список для записи информации.
        """
        SYMBOL_SIZE = 20
        if len(matrix) != 0:
            lenght = None
            for i in range(len(matrix)):
                string = "".join([str(f)+" "*(SYMBOL_SIZE-len(str(f))) for f in matrix[i]])
                print(string)
                lenght = len(string)
            print("-" * lenght)
        else:
            print("Решений нет")
        return

    def simplex_method(self, max=True):
        """
        Симплекс метод решения задачи линейного програмирования.
        :param SIMPLEX_TABLE: симплекс таблица составленная из условий.
        :return: информация об проделанных операциях.
        """

        SIMPLEX_TABLE = self.find_start_plan()
        if not max:
            for i in range(len(SIMPLEX_TABLE[0])):
                SIMPLEX_TABLE[0][i] = 0 - SIMPLEX_TABLE[0][i]
        #self.matrix_print(SIMPLEX_TABLE)

        info = [True, 0, 0]
        iteration_count = 0
        while info[0]:
            iteration_count += 1
            info = self.__check_vector(SIMPLEX_TABLE[0])
            if not info[0]:
                break
            min = 10 ** 100
            index = -1
            for i in range(1, len(SIMPLEX_TABLE)):
                if SIMPLEX_TABLE[i][info[1]] > 0:
                    c = SIMPLEX_TABLE[i][0]/SIMPLEX_TABLE[i][info[1]]
                    if c < min:
                        min = c
                        index = i
            if index == -1:
                return False
            self.one_replace(SIMPLEX_TABLE, info[1], index)
            #self.matrix_print(SIMPLEX_TABLE)

        self.__optimal_table = copy.copy(SIMPLEX_TABLE)
        self.__optimal_value = SIMPLEX_TABLE[0][0]
        return True

    def __check_vector(self, C):
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
        return info