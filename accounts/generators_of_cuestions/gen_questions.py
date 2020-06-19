import random
import math
from app.models import Answer


class GeneratorQuestions(object):
    @classmethod
    def generate_question(cls):
        # генерируем произвальные значения для задания
        nom_z, test_id, colvo_z = 1, "1234567", 1
        random_var(cls)
        # вычисляем решение
        reshenie(cls)
        # тут вызывется фунция создания вариантов ответа и результат присваивается переменным
        var_a, var_b, var_c, var_d, prav_otv = variants(cls)
        # Тут вызывается функци для формирования текста задания
        text_zad = zadaine(cls)
        # Тут на основе ID, номера задания, количества формируется имя файла с готовым заданием в формате html
        z_path = "{test_id}_{nom_z}_{colvo_z}.html".format(
            nom_z=nom_z, colvo_z=colvo_z, test_id=test_id
        )

        response_data = {
            'id': test_id,
            'nom_z': nom_z,
            'colvo_z': colvo_z,
            'text': text_zad,
            'variable_answers': [var_a, var_b, var_c, var_d],
            'truly_answer': prav_otv,
            'z_path': z_path
        }

        return response_data


    @classmethod
    def generate_question_two(cls):
        # Генерируем сторону квадарата
        row_of_square = random.randint(3, 10)
        # Генерируем квадарат
        N = row_of_square * row_of_square
        answer = int(math.log2(N))
        cls.a = answer
        ansers = generate_random_variables(answer)
        # Генерируем текст задачи
        text = zadaine_type_2(cls)
        nom_z, test_id, colvo_z = 1, "1234567", 1
        z_path = "{test_id}_{nom_z}_{colvo_z}.html".format(
            nom_z=nom_z, colvo_z=colvo_z, test_id=test_id
        )

        response_data = {
            'id': test_id,
            'nom_z': nom_z,
            'colvo_z': colvo_z,
            'text': text,
            'variable_answers': ansers[0:4],
            'truly_answer': ansers.index(answer),
            'z_path': z_path
        }
        return response_data


    @classmethod
    def generate_question_four(cls):
        # Создаем массив чисел с основнием 2, для удобного счета
        arr = [2 ** i for i in range(7)]
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
        answer = int(math.log2(1 / p))
        # Генерируем набор ответов
        anwsers = generate_random_variables(answer)
        # Генерируем текст задачи
        text = zadaine_type_3(cls)
        # Генерируем номер задачи, id теста
        nom_z, test_id, colvo_z = 1, "1234567", 1
        z_path = "{test_id}_{nom_z}_{colvo_z}.html".format(
            nom_z=nom_z, colvo_z=colvo_z, test_id=test_id
        )

        # Словарь с сгенерированными данными
        response_data = {
            'id': test_id,
            'nom_z': nom_z,
            'colvo_z': colvo_z,
            'text': text,
            'variable_answers': anwsers[0:4],
            'truly_answer': anwsers.index(answer),
            'z_path': z_path
        }
        return response_data