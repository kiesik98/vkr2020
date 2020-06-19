import json

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from accounts.forms import UserLoginForm
from app import forms as app_forms
from app.scripts.generate_question import QuestionTemplate
from app.models import Topic, TopicQuestion, StudentTest, User, Question, StudentAnswer, Test
from django.contrib import messages



def login_view(request):
    # next_page = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        # if next_page:
        #     redirect(next_page)
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, "custom_login.html", context)


def signup_view(request):
    if request.method == 'POST':
        form = app_forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('admin:index')
    else:
        form = app_forms.SignUpForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('http://user123.pythonanywhere.com')


def generate_view(request):
    """Генерация нового вопроса"""
    # Тип задачи
    taskType = int(request.POST['taskType'])
    # Тема задачи
    topicValue = request.POST['topicValue']

    try:
        topic = Topic.objects.get(pk=int(topicValue))
    except ValueError:
        topic = Topic.objects.get_or_create(name=topicValue)[0]
        topic.save()

    # Для автоматически сгенерированных значений всегда единичный ответ
    obj = TopicQuestion(topic=topic, answer_type='SINGLE')
    # Создаем инстанс вопроса, делее заполним его поля
    obj.save()

    QuestionTemplate.create_question(obj, taskType)
    messages.info(request, 'Сгенерированный вопрос успешно добавлен')
    response = {'message': 'Сгенерированный вопрос успешно добавлен', 'status': 200}

    return HttpResponse(json.dumps(response), content_type='application/json')


def results_analitics_view(request,pk):
    if pk:
        students_test = StudentTest.objects.filter(test_id=pk)
    else:
        students_test = StudentTest.objects.first()

    all_questions = Question.objects.filter(test_id=pk).count()

    answer_list = []
    for row in students_test:
        test = StudentTest.objects.filter(id=row.id).first()
        answers = StudentAnswer.objects.filter(question__test_id=row.id)
        nice_answers = list(answers.filter(answers__right=True).values_list('question_id', flat=True))
        errors = list(answers.filter(answers__right=False).values_list('question_id', flat=True))
        answer_list.append(
            {
                'points': test.points,
                'name': f"{row.student.last_name} {row.student.first_name} {row.student.middle_name}",
                'test_count_questions': StudentAnswer.objects.filter(question__test_id=row.id).count(),
                'nice_answers': ','.join([str(i) for i in nice_answers]),
                'nice_answers_count': len(nice_answers),
                'errors': ','.join([str(i) for i in errors]),
                'all_questions_count': str(all_questions)
            })
    recipe_list_json = json.dumps(answer_list)

    return JsonResponse(recipe_list_json, safe=False)


def delete(request):
    Question.objects.filter(text='').delete()
    messages.info(request, 'Сгенерированный вопрос успешно добавлен')

    response = {'message': 'Некорректные записи успешно удалены', 'status': 200}
    return HttpResponse(json.dumps(response), content_type='application/json')
