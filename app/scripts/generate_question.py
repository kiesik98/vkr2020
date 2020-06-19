# coding: utf-8

import random
import math
from app.models import Answer
from app.scripts.texts import texts
from fractions import Fraction
from math import copysign, fabs, frexp, isfinite, ldexp, modf
import sys


# Основные переменные для работы шаблона задания
class QuestionTemplate:  # Все переменные хранятся здесь обращение к ним чрез question.a
    type = None  # тип задания 1 - практическое, 2 - теоретическое (для разделения на типы может быть)
    # список для сохранения сгенерированных для задания чисел. Нужно чтобы числа не повторялись
    chisla = []

    # Основные переменные задания для инициализации присвоено значение None далее работает Random можно добавить больше или убрать лишние
    a = None
    b = None
    c = None
    d = None
    e = None
    f = None

    # результат задания всегда присаивается переменной rez_z
    rez_z = None

    @staticmethod
    def generate_bin():
        return bin(random.randint(10, 30)).split('b')[1]


    @staticmethod
    def toFixed(num, digits=0):
        return f"{num:.{digits}f}"

    @staticmethod
    def convert_base(num, to_base=10, from_base=10):
        # Конвертация в любую системы счисления из любой
        if isinstance(num, str):
            n = int(num, from_base)
        else:
            n = int(num)
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if n < to_base:
            return alphabet[n]
        else:
            return QuestionTemplate.convert_base(n // to_base, to_base) + alphabet[n % to_base]

    @staticmethod
    def rand_key(p):
        key1 = ""
        for i in range(p):
            temp = str(random.randint(0, 1))
            key1 += temp
        return(key1)

    @staticmethod
    def remove_char(string, n):
        string = list(string)
        string.remove(n)
        return ''.join(string)

    @staticmethod
    def nod(a,b):
        while a != 0 and b != 0:
            # сравнивать их между собой.
            # Если первое число больше второго,
            if a > b:
                # то находить остаток от деления его на второе число
                # и присваивать его первой переменной
                a = a % b
            # Иначе (когда второе число больше первого)
            else:
                # присваивать второй переменной остаток от деления
                # нацело второго числа на первое
                b = b % a

        # Одно из чисел содержит 0, а другое - НОД, но какое - неизвестно.
        # Проще их сложить, чем писать конструкцию if-else
        itog = a + b
        return itog


    @staticmethod
    def float_to_bin(f):
        # NOTE: the implementation closely follows float.hex()
        if not isfinite(f):
            return repr(f)  # inf nan

        sign = '-' * (copysign(1.0, f) < 0)
        if f == 0:  # zero
            return sign + '0b0.0p+0'

        # f = m * 2**e
        m, e = frexp(fabs(f))  # 0.5 <= m < 1.0
        shift = 1 - max(sys.float_info.min_exp - e, 0)
        m = ldexp(m, shift)  # m * (2**shift)
        e -= shift

        fm, im = modf(m)
        assert im == 1.0 or im == 0.0
        n, d = fm.as_integer_ratio()
        assert d & (d - 1) == 0  # power of two
        return '{sign}0b{i}.{frac:0{width}b}p{e:+}'.format(
            sign=sign, i=int(im), frac=n, width=d.bit_length() - 1, e=e)



    @classmethod
    def create_question(cls, obj, taskType):
        """Метод генерирующий вопросы и ответы по типам задачи

        Arg:
            obj (TopicQuestion): Объекто вопроса
            taskType (str): Тип генерируемой задачи
        """
        dict_of_types = {
            1: QuestionTemplate.generate_question,
            2: QuestionTemplate.generate_question_two,
            4: QuestionTemplate.generate_question_four,
            5:  QuestionTemplate.generate_question_five,
            6:  QuestionTemplate.generate_question_six,
            7:  QuestionTemplate.generate_question_seven,
            8:  QuestionTemplate.generate_question_8,
            9:  QuestionTemplate.generate_question_9,
            10:  QuestionTemplate.generate_question_10,
            11:  QuestionTemplate.generate_question_11,
            12: QuestionTemplate.generate_question_12,
            13: QuestionTemplate.generate_question_13,
            14: QuestionTemplate.generate_question_14,
            15: QuestionTemplate.generate_question_15,
            16: QuestionTemplate.generate_question_16
        }
        generated_data = dict_of_types[taskType]()
        obj.text = generated_data['text']
        answers = []
        if 'variable_answers' in generated_data:
            for i in generated_data['variable_answers']:
                right = generated_data['truly_answer'] == i
                answers.append(Answer(text=i, right=right, question=obj))
        Answer.objects.bulk_create(answers)
        obj.save()

    @classmethod
    def generate_question(cls):
        # генерируем произвальные значения для задания
        len_text = random.randint(1,80)
        litera = random.randint(1, len_text)
        P = litera / len_text
        answer = round(int(math.log2(1/P)))
        answers = generate_random_variables(answer)

        # Тут вызывается функци для формирования текста задания
        text = texts(1, len_text, litera)

        random.shuffle(answers)

        return get_response_date(answers, answer, text)

    @classmethod
    def generate_question_two(cls):
        # Генерируем сторону квадарата
        row_of_square = random.randint(3, 10)
        # Генерируем квадарат
        answer = int(math.log2(row_of_square**2))
        answers = generate_random_variables(answer)
        # Генерируем текст задачи
        text = texts(2, answer)

        return get_response_date(answers, answer, text)

    @classmethod
    def generate_question_four(cls):
        # Создаем массив чисел с основнием 2, для удобного счета
        arr = [2**i for i in range(7)]
        # Выьраем рандомное число из созданного массива
        count = random.choice(arr)
        # Делаем срез для выбора меньшего подмассива. Т.к выбранное число не может быть больше общего числа объектов
        less = arr[:arr.index(count)]
        # Выбор меньшего числа из созданного подмассива
        selected = random.choice(less)
        # Вычисление вероятности
        p = selected / count
        cls.a = count
        cls.b = selected
        # Получаем ответ
        answer = int(math.log2(1/p))
        # Генерируем набор ответов
        answers = generate_random_variables(answer)
        # Генерируем текст задачи
        text = texts(4, cls.a, cls.b)

        return get_response_date(answers, answer, text)


    @classmethod
    def generate_question_five(cls):
        # А1
        # 2 формы: a)1 b)1
        base = random.randint(11, 16)
        num = random.randint(100, 999)
        word_1 = cls.convert_base(num, to_base=base)

        base2 = random.randint(3, 9)
        a = random.randint(1, 9)
        a1 = random.choice([base2**1, base2**2, base2**3])
        num2 = Fraction(a, a1)
        b1 = cls.convert_base(a, to_base=base2)
        b2 = cls.convert_base(a1, to_base=base2)
        c1 = int(b1)
        c2 = int(b2)
        word_2 = Fraction(c1,c2)
        word_3 = c1/c2
        if (word_3 % 1) == 0:
            word_3 = word_3 // 1
            word_3 = int(word_3)

        cls.a = base
        cls.b = num
        cls.c = base2
        cls.d = num2
        # Получаем ответ

        answer = f'{word_1}, {word_3}'
        # Генерируем текст задачи
        text = texts(5, num, base, num2, base2)

        # Словарь с сгенерированными данными
        response_data = {
            'text': text,
            'variable_answers': [answer],
            'truly_answer': answer
        }

        return response_data

    @classmethod
    def generate_question_six(cls):
        # А2 Перевод из n-ой системы счисления в десятичную
        # 4 формы: a)1 b)3

        base = random.randint(11, 16)
        num = random.randint(100, 999)
        num = str(num)
        word_1 = cls.convert_base(num, from_base=base)

        base2 = random.randint(2, 9)
        a = random.randint(0, base2-1)
        a1 = random.randint(0, base2-1)
        a2 = random.randint(0, base2-1)
        a3 = random.randint(1, base2-1)
        num2 = a+a1/10+a2/100+a3/1000
        num2 = cls.toFixed(num2, digits=3)
        z = (a * base2 ** 0) + (a1 * base2 ** -1) + (a2 * base2 ** -2) + (a3 * base2 ** -3)
        z3 = z
        z3 = cls.toFixed(z3, digits=3)
        z3 = float(z3)
        a4 = z3-float(a)
        a4 = cls.toFixed(a4, digits=3)

        z2 = z-a
        z2 = cls.toFixed(z2, digits=3)
        z2 = float(z2)
        z4 = z3-z2
        z4 = int(z4)
        word_3 = (z - z4) * (base2 ** 3)
        word_3 = cls.toFixed(word_3, digits=0)
        z = cls.toFixed(z, digits=3)
        word_2 = z
        word_4 = base2 ** 3
        '''
        a = str(a)
        c1 = int(b1)
        c2 = int(b2)
        c2 = c2/1000
        word_2 = c1+c2 '''
        cls.a = base
        cls.b = num
        cls.c = base2
        cls.d = num2

        answer = f'{word_1}, {z4}, {word_3}, {word_4}'
        # Получаем ответ
        # Генерируем текст задачи
        text = texts(6, num, base, num2, base2)
        # Словарь с сгенерированными данными
        response_data = {
            'text': text,
            'variable_answers': [answer],
            'truly_answer': answer
        }

        return response_data

    @classmethod
    def generate_question_seven(cls):
        # А3
        # 2 формы: a)1 b)1
        final1 = 0
        final2 = 0
        while (final1 == 0):
            num = cls.rand_key(5)
            if num[0] == '1':
                final1 = -1 * (int(''.join('1' if x == '0' else '0' for x in num), 2) + 1)
        while (final2 == 0):
            num2 = cls.rand_key(5)
            if num2[0] == '0':
                final2 = int(num2, 2)
        cls.a = num
        cls.b = num2
        # Получаем ответ
        answer = f'{final1}, {final2}'
        # Генерируем текст задачи
        text = texts(7, num, num2)

        response_data = {
            'text': text,
            'variable_answers': [answer],
            'truly_answer': answer
        }
        return response_data

    @classmethod
    def generate_question_8(cls):
        # А4
        # 2 формы: a)1 b)1
        num = random.randint(0, 127)
        num2 = random.randint(-128,-1)
        if num>=0:
                bin1 = bin(num).split("0b")[1]
                while len(bin1)<8:
                        bin1 = '0'+bin1
                answer1 = bin1
        if num2<=0:
                bin1 = -1*num2
                answer2 = bin(bin1-pow(2,8)).split("0b")[1]
        cls.a = num
        cls.b = num2

        answer = f'{answer1}, {answer2}'

        text = texts(8, num, num2)

        response_data = {
            'text': text,
            'variable_answers': [answer],
            'truly_answer': answer
        }
        return response_data

    @classmethod
    def generate_question_9(cls):
        # A5
        # 3 формы с чекбоксами: a)1х b)1х c)1x
        final1 = 0
        final2 = 0
        final3 = 0
        while (final1 == 0):
            num = cls.rand_key(4)
            num2 = cls.rand_key(4)
            if num[0] == '0' and num2[0] == '0':
                finala = str(num)+'+'+str(num2)
                integer_sum1 = int(num, 2) + int(num2, 2)
                final1 = bin(integer_sum1).split("0b")[1]
                while len(final1)<4:
                    final1 = '0'+final1
        while (final2 == 0):
            num = cls.rand_key(4)
            num2 = cls.rand_key(4)
            if num[0] == '1' and num2[0] == '1':
                finalb = str(num)+'+'+str(num2)
                integer_sum2 = (-1 * (int(''.join('1' if x == '0' else '0' for x in num), 2) + 1)) + -1 * (int(''.join('1' if x == '0' else '0' for x in num2), 2) + 1)
                bin1 = -1*integer_sum2
                final2 = bin(bin1-pow(2,4)).split("0b")[1]
                while len(final2)<4:
                        final2 = '0'+final2
        while (final3 == 0):
            num = cls.rand_key(4)
            num2 = cls.rand_key(4)
            if (num[0] == '1' and num2[0] == '0'):
                finalc = str(num)+'+'+str(num2)
                integer_sum3 = (-1 * (int(''.join('1' if x == '0' else '0' for x in num), 2) + 1)) + int(num2, 2)
                if integer_sum3>=0:
                    final3 = bin(integer_sum3).split("0b")[1]
                    while len(final3)<4:
                        final3 = '0'+final3
                else:
                    bin1 = -1*integer_sum3
                    final3 = bin(bin1-pow(2,4)).split("0b")[1]
            elif (num[0] == '0' and num2[0] == '1'):
                finalc = str(num)+'+'+str(num2)
                integer_sum3 = int(num, 2) + (-1 * (int(''.join('1' if x == '0' else '0' for x in num2), 2) + 1))
                if integer_sum3>=0:
                    final3 = bin(integer_sum3).split("0b")[1]
                    while len(final3)<4:
                        final3 = '0'+final3
                else:
                    bin1 = -1*integer_sum3
                    final3 = bin(bin1-pow(2,4)).split("0b")[1]
        if integer_sum1 > 7:
            check1 = 1
        else:
            check1 = 0
        if integer_sum2 < -8:
            check2 = 1
        else:
            check2 = 0
        check3 = 0
        cls.a = num
        cls.b = num2
        # Получаем ответ
        # Генерируем набор ответов
        answer = f'{final1}, {check1}, {final2}, {check2}, {final3}, {check3}'
        # Генерируем текст задачи
        text = texts(9, finala, finalb, finalc)

        response_data = {
            'text': text,
            'variable_answers': [answer],
            'truly_answer': answer
        }
        return response_data

    @classmethod
    def generate_question_10(cls):
        # A6
        # 9 форм: a)3 b)3 c)3
        num2 = random.randint(1, 8)
        num = random.choice([i for i in range(0, 7) if i < num2])
        num4 = random.randint(0, 7)
        num3 = random.choice([i for i in range(0, 8) if i > num4])
        numfinal = random.randint(1, 2)
        final11 = 0
        final12 = 0
        final13 = 0
        final21 = 0
        final22 = 0
        final23 = 0
        final31 = 0
        final32 = 0
        final33 = 0
        while (final11 == 0) and (final12 == 0) and (final13 == 0):
            bin1 = bin(num).split("0b")[1]
            while len(bin1)<4:
                bin1 = '0'+bin1
            final11 = bin1
            bin2 = bin(num2).split("0b")[1]
            while len(bin2)<4:
                bin2 = '0'+bin2
            final12 = bin2
            bin10 = num-num2
            bin3 = -1*bin10
            final13 = bin(bin3-pow(2,4)).split("0b")[1]
            while len(final13)<4:
                    final13 = '0'+final13
        while (final21 == 0) and (final22 == 0) and (final23 == 0):
            bin1 = bin(num3).split("0b")[1]
            while len(bin1)<4:
                bin1 = '0'+bin1
            final21 = bin1
            bin2 = bin(num4).split("0b")[1]
            while len(bin2)<4:
                bin2 = '0'+bin2
            final22 = bin2
            bin3 = bin(num3-num2).split("0b")[1]
            while len(bin3)<4:
                bin3 = '0'+bin3
            final23 = bin3
        while (final31 == 0) and (final32 == 0) and (final33 == 0):
            if numfinal == 1:
                num51 = random.randint(-8, -1)
                num52 = random.randint(-8, -1)
                minusnum = num51+num52

                bin1 = -1*num51
                final31 = bin(bin1-pow(2,4)).split("0b")[1]

                bin2 = -1*num52
                final32 = bin(bin2-pow(2,4)).split("0b")[1]


                bin3 = -1*minusnum
                final33 = bin(bin3-pow(2,4)).split("0b")[1]
                while len(final33)<4:
                        final33 = '0'+final33
            else:
                num51 = random.randint(0, 7)
                num52 = random.randint(0, 7)
                bin1 = bin(num51).split("0b")[1]
                while len(bin1)<4:
                    bin1 = '0'+bin1
                final31 = bin1
                bin2 = bin(num52).split("0b")[1]
                while len(bin2)<4:
                    bin2 = '0'+bin2
                final32 = bin2
                plusnum = num51+num52
                bin3 = bin(plusnum).split("0b")[1]
                while len(bin3)<4:
                    bin3 = '0'+bin3
                final33 = bin3


        cls.a = num
        cls.b = num2
        cls.c = num3
        cls.d = num4
        cls.e = num51
        cls.f = num52
        # Получаем ответ

        # Генерируем набор ответов
        answer = f'{final11}, {final12}, {final13}, {final21}, {final22}, {final23}, {final31}, {final32}, {final33}'
        # Генерируем текст задачи
        text = texts(10, num, num2, num3, num4, num51, num52)
        response_data = {
            'text': text,
            'variable_answers': [answer],
            'truly_answer': answer
        }
        return response_data

    @classmethod
    def generate_question_15(cls):
        # А7
        # 2 форм a)1 b)1
        word_1 = 0
        word_2 = 0
        bin1 = 0
        bin2 = 0
        cls.a = bin1
        cls.b = bin2
        while (word_1 == 0):
            num = cls.rand_key(8)
            if num[0] == '0' and (num[1]+num[2]+num[3] != '000' and num[1]+num[2]+num[3] != '111'):
                bin1 = num
                baz = (int(num[1]) * (2 ** 2)) + (int(num[2]) * (2 ** 1)) + (int(num[3]) * (2 ** 0))
                baz2 = int(baz)
                word_1 = (1 * (2 ** 0) + (int(num[4]) * (2 ** -1)) + (int(num[5]) * (2 ** -2)) + (int(num[6]) * (2 ** -3)) + (int(num[7]) * (2 ** -4))) * (2 ** (baz2-3))
        while (word_2 == 0):
            num2 = cls.rand_key(8)
            if num2[0] == '1' and (num2[1]+num2[2]+num2[3] != '000' and num2[1]+num2[2]+num2[3] != '111'):
                bin2 = num2
                raz = (int(num2[1]) * (2 ** 2)) + (int(num2[2]) * (2 ** 1)) + (int(num2[3]) * (2 ** 0))
                raz2 = int(raz)
                dva = raz2 - 3
                word_2 = (1 * (2 ** 0) + (int(num2[4]) * (2 ** -1)) + (int(num2[5]) * (2 ** -2)) + (int(num2[6]) * (2 ** -3)) + (int(num2[7]) * (2 ** -4))) * (2 ** dva)
                word_2 = -1 * word_2
        answer = f'{word_1}, {word_2}'

        # Генерируем текст задачи
        text = texts(15, bin1, bin2)

        response_data = {
            'text': text,
            'variable_answers': [answer],
            'truly_answer': answer
        }
        return response_data



    @classmethod
    def generate_question_16(cls):
        #A8
        c =''
        c2 =''
        celoe = random.randint(0,15)
        celoe2 = random.randint(-15, -1)
        znam = random.choice([2 ** i for i in range(1,6)])
        znam2 = random.choice([2 ** i for i in range(1,6)])
        chislitel = random.choice([i for i in range(0, 64) if i < znam])
        chislitel2 = random.choice([i for i in range(0, 64) if i < znam2])
        nod1 = cls.nod(chislitel, znam)
        nod2 = cls.nod(chislitel2, znam2)
        if nod1>1:
            chislitel = chislitel/nod1
            chislitel = int(chislitel)
            znam = znam/nod1
            znam = int(znam)
        if nod2>1:
            chislitel2 = chislitel2/nod2
            chislitel2 = int(chislitel2)
            znam2 = znam2/nod2
            znam2 = int(znam2)
        if chislitel == 0:
            znam = 0
            c =('0000')
        else:
            x = chislitel
            y = znam
            while y!= 1:
                if y/2>x:
                    c+='0'
                    y=y/2
                else:
                    c+='1'
                    y=y/2
                    x=x-y
                while len(c) < 4:
                    c = c+'0'
        if chislitel2 == 0:
            znam2 = 0
            c2 =('0000')
        else:
            x2 = chislitel2
            y2 = znam2
            while y2!= 1:
                if y2/2>x2:
                    c2+='0'
                    y2=y2/2
                else:
                    c2+='1'
                    y2=y2/2
                    x2=x2-y2
                while len(c2) < 4:
                    c2 = c2+'0'
        ps_bin=bin(celoe)[2:]
        celoe2=-1*celoe2
        ps_bin2=bin(celoe2)[2:]
        while len(ps_bin) < 4:
            ps_bin = '0'+ps_bin
        while len(ps_bin2) < 4:
            ps_bin2 = '0'+ps_bin2
        full_bin=str(ps_bin+'b'+str(c))
        full_bin2=str(ps_bin2+'b'+str(c2))
        seredina=full_bin.find('b')
        seredina2=full_bin2.find('b')
        full_bin = cls.remove_char(full_bin, 'b')
        full_bin2 = cls.remove_char(full_bin2, 'b')
        first_number=full_bin.find('1')
        first_number2=full_bin2.find('1')
        normalize = int(seredina)-int(first_number)-1
        normalize2 = int(seredina2)-int(first_number2)-1
        others = int(first_number)+1
        others2 = int(first_number2)+1
        others4 = int(others) + 4
        others42 = int(others2) + 4
        mantissa = full_bin[others:others4]
        while len(mantissa) < 4:
            mantissa = mantissa +'0'
        mantissa2 = full_bin2[others2:others42]
        while len(mantissa2) < 4:
            mantissa2 = mantissa2 +'0'
        exponent = normalize+3
        exponent2 = normalize2+3
        bin_expo = bin(exponent)[2:]
        while len(bin_expo) < 3:
            bin_expo = '0'+bin_expo
        bin_expo2 = bin(exponent2)[2:]
        while len(bin_expo2) < 3:
            bin_expo2 = '0'+bin_expo2
        final = '0' + bin_expo + mantissa
        final2 = '1' + bin_expo2 + mantissa2
        celoe2 = -1*celoe2

        answer = f'{final}, {final2}'

        # Генерируем текст задачи
        text = texts(16, celoe, chislitel, znam, celoe2, chislitel2, znam2)

        response_data = {
            'text': text,
            'variable_answers': [answer],
            'truly_answer': answer
        }
        return response_data



    @classmethod
    def generate_question_11(cls):
        # A9 Бросок игральных костей
        num = random.choice([i for i in range(8)])

        cost = 6
        monet = 2
        num2 = random.choice([i for i in range(8)])

        #  возможные варианты монеты
        answers = ['0.5 бит, 1/3 log^2 6 бит', '2 бит, 4 log^2 10 бит', '1 бит, 1/6 log^2 6 бит', '4 бит, 16 бит']

        answer = answers[2]

        random.shuffle(answers)
        cls.a = num
        cls.b = num2
        # Получаем ответ

        # Генерируем текст задачи
        text = texts(11, cls.a, cls.b)

        return get_response_date(answers, answer, text)

    @classmethod
    def generate_question_12(cls):
        # Б1
        # Длинны слов

        answer = None
        false_answer = None

        while not answer:
            L = [random.randint(1, 10) for _ in range(4, random.randrange(5,10))]
            # Размерность алфавита
            q = random.choice([2,3,4])

            summ = 0
            # Вычислем сумму степеней
            for i in L:
                summ += q ** (-i)

            if summ <= 1:
                answer = (L, q)
            else:
                if not false_answer:
                    false_answer = str((L, q))

        falses = []
        while len(falses) <= 2:
            while not false_answer:
                L = [random.randint(1, 10) for _ in range(4, random.randrange(5, 10))]
                # Размерность алфавита
                q = random.choice([2, 3, 4])

                summ = 0
                # Вычислем сумму степеней
                for i in L:
                    summ += q ** (-i)

                if summ >= 1:
                    false_answer = (L, q)

            if false_answer not in falses:
                falses.append(false_answer)
            false_answer = None

        falses.append(answer)
        random.shuffle(falses)

        # Перемешиваем
        cls.a = random.choice([answer, false_answer])
        cls.b = false_answer if cls.a == answer else answer

        # Генерируем текст задачи
        text = texts(12, *falses)

        return get_response_date(falses, answer, text)

    @classmethod
    def generate_question_13(cls):
        # Б2
        # ФАНО
        # Вероятность
        P = [float(f"%.2f" % random.uniform(0,1)) for _ in range(random.randrange(6,9))]

        sorted(P, reverse=True)
        Shannon_Fano_list = []

        # Рекурсия
        Shannon_Fano_coding(P,'', Shannon_Fano_list)

        # Генерируем текст задачи
        random.shuffle(P)
        text = texts(13, P)

        summ_of_symbols = 0
        for i in Shannon_Fano_list:
            summ_of_symbols += len(i)

        l = len(P)
        N = 0 # Возможное кол-во сигналов
        K = 2 # Основниае системы счисления
        m = 0 # среднее число элементарных символов на букву

        while N <= l:
            N = K**m
            m += 1

        middle_coding_by_Fano = "%.2f" % (summ_of_symbols / len(Shannon_Fano_list))
        answer = [Shannon_Fano_list, float(middle_coding_by_Fano), float(m)]
        answer_template = f"Код Фано {''.join(Shannon_Fano_list)}. Средняя длина кода по Фано {middle_coding_by_Fano}. Средняя линейная длина кода {m}"

        answers = []
        for i in range(4):
            Shannon_Fano_list, middle_coding_by_Fano, m = answer
            fake_fano = []
            dd = []
            for i in Shannon_Fano_list:
                dd.extend(generate_random_variables(i, bin=True, len_bin=len(i)))
            fake_fano.extend(dd)

            fake_fano = fake_fano[0: len(Shannon_Fano_list)]
            fake_fano_middle = float("%.2f" % random.uniform(0,1)) + random.uniform(
                middle_coding_by_Fano - float(middle_coding_by_Fano)/2,
                middle_coding_by_Fano + float(middle_coding_by_Fano)/2
            )

            fake_middle_line = random.randint(
                    int(m - m/2),
                    int(m + middle_coding_by_Fano/2)
                )

            # Если сгенерированы совпадения - сбрасываем
            if fake_middle_line == m or fake_fano_middle == middle_coding_by_Fano:
                return cls.generate_question_13()

            fake_fano_middle = "%.2f" % fake_fano_middle

            ans = f"Код Фано {''.join(fake_fano)[0:len(''.join(Shannon_Fano_list))]}. Средняя длина кода по Фано { fake_fano_middle}. Средняя линейная длина кода {fake_middle_line}"

            if ans == "":
                return cls.generate_question_13()

            answers.append(ans)

        answers.append(answer_template)

        return get_response_date(answers, answer_template, text)

    @classmethod
    def generate_question_14(cls):
        from app.scripts.Hemming import Hemming
        # Б3
        # Хемминг

        # r - степень, которой определяется количество битов в сообщении
        r = 3
        k = 2 ** r - r - 1

        # 1 часть
        word_1_base = cls.generate_bin()
        word_1 = word_1_base
        # Вычисдение числа нужных доп битов
        m = len(word_1_base)
        r = Hemming.calcRedundantBits(m)

        # Определение позиции доп. битов
        arr = Hemming.posRedundantBits(word_1_base, r)
        # Опеределение битов четности
        arr = Hemming.calcParityBits(arr, r)
        word_1_ans = arr

        # print('Задумано',word_1_base )
        # print('Получено',word_1_ans )


        if len(word_1) % k != 0:
            word_1 += '0' * (k - (len(word_1) % k))

        other_answers = generate_random_variables(word_1, bin=True, len_bin=len(word_1))

        data = cls.generate_bin()
        # Вычисдение числа нужных доп битов
        m = len(data)
        r = Hemming.calcRedundantBits(m)

        # Определение позиции доп. битов
        arr = Hemming.posRedundantBits(data, r)
        # Опеределение битов четности
        arr = Hemming.calcParityBits(arr, r)
        ans = arr

        arr = list(arr)

        # Добавляем ошибку
        arr[3] = '0' if arr[1] else '1'

        arr = ''.join(arr)
        fake = arr

        # correction = Hemming.detectError(fake, r)
        # print('Переданое сообщение', ans)
        # print('Переданное сообщение с ошибкой', fake)
        # print('Позиция ошибки(ошибки считаютс в обратном порядке)', correction)

        text = texts(14, word_1_base, fake)
        answer = f'{word_1}, {word_1_ans}'

        # Словарь с сгенерированными данными
        response_data = {
            'text': text,
            'variable_answers': [answer],
            'truly_answer': answer
        }

        return response_data




def correct_generator():
    # Генерируем знак +/-
    sym = random.randint(0, 1)
    # Порядок Смещения
    ps = random.randint(1, 4)
    # Значение
    value_gen = random.randint(1, 16)

    # Смещение
    ps_bin = bin(ps)[2:]
    while len(ps_bin) < 3:
        ps_bin = '0' + ps_bin

    val_bin = str(str(sym) + ps_bin + str(bin(value_gen)[2:]))[:8]

    while len(val_bin) < 8:
        val_bin = val_bin + '0'

    # Знак
    znak = True if val_bin[0] == '1' else False
    # Знак
    k = val_bin[1:4]
    mantiss = val_bin[4:]
    por = int(k, 2)

    # Фрмируем значение в виде числа с плавающей точкой
    value = ''
    if znak:
        value += '-'

    if por > len(mantiss):
        # Целая часть
        cel = int(mantiss, 2)
    else:
        try:
            cel = int(mantiss[:por], 2)
            # Дробная часть
            rat = int(mantiss[por:], 2)

            # Если ошибка, по-новое генерим
        except:
            return correct_generator()

    value += str(cel)

    if por < len(mantiss):
        value += '.' + str(rat)

    return value, val_bin


def Shannon_Fano_coding(seq, code, Shannon_Fano_list):
    a = []
    b = []
    if len(seq) == 1:
        Shannon_Fano_list.append(code)
        return 0
    for idx, i in enumerate(seq):
        if sum(a) < sum(b):
            a.append(i)
        else:
            b.append(i)
            # b[idx] = i
    Shannon_Fano_coding(a, code + "0", Shannon_Fano_list)
    Shannon_Fano_coding(b, code + "1", Shannon_Fano_list)


def generate_random_variables(answer, bin=False, len_bin=None, max_int=None):
    data = []
    while len(data) < 3:
        if not bin:
            val = random.randint(1, max_int or 20)
            if val not in data and val != answer:
                data.append(val)
        else:
            val = ''.join([str(random.randint(0,1)) for i in range(len_bin or 8)])

            if val != answer and val not in data:
                data.append(val)

    data.append(answer)
    random.shuffle(data)

    return data


def get_response_date(answers, answer, text):
    return {
        'text': text,
        'variable_answers': answers,
        'truly_answer': answer,
    }

question = QuestionTemplate()