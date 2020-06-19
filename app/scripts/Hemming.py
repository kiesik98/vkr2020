import  random

class Hemming(object):


    @staticmethod
    def calcRedundantBits(m):
        # Используется формула 2 ^ r >= m + r + 1
        # для вычисления дополнительных битов.
        # Итерируем 0 .. m и возвращаем значение
        for i in range(m):
            if (2 ** i >= m + i + 1):
                return i

    @staticmethod
    def posRedundantBits(data, r):
        # резервировные биты размещаются на  позициях
        # которые соответствуют степени 2
        j = 0
        k = 1
        m = len(data)
        res = ''

        # Если позиция - степень 2, тогда вставьте '0'
        # Или добавить данные
        for i in range(1, m + r + 1):
            if (i == 2 ** j):
                res = res + '0'
                j += 1
            else:
                res = res + data[-1 * k]
                k += 1

        return res[::-1]

    @staticmethod
    def calcParityBits(arr, r):
        n = len(arr)
        for i in range(r):
            val = 0
            for j in range(1, n + 1):
                if (j & (2 ** i) == (2 ** i)):
                    val = val ^ int(arr[-1 * j])

            # (0 to n - 2^r) + четный бит + (n - 2^r + 1 to n)
            arr = arr[:n - (2 ** i)] + str(val) + arr[n - (2 ** i) + 1:]
        return arr

    @staticmethod
    def detectError(arr, nr):
        n = len(arr)
        res = 0

        for i in range(nr):
            val = 0
            for j in range(1, n + 1):
                if (j & (2 ** i) == (2 ** i)):
                    val = val ^ int(arr[-1 * j])

            res = res + val * (10 ** i)

        return int(str(res), 2)


    @staticmethod
    def add_error(code):
        l = list(code)
        error_diapazone = 4
        l[error_diapazone] = str(0) if l[error_diapazone] else str(1)

        return l
