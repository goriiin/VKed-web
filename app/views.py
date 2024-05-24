from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from app import model_manager


def index(request):
    context = model_manager.pagination(request, 'index')
    print(context)
    return render(request, 'index.html', context)


def hot(request):
    context = model_manager.pagination(request, 'hot')
    return render(request, 'hot.html', context)


def question(request, question_id):
    context = model_manager.this_question(request, question_id)
    form = model_manager.get_answer_form(request)
    context['form'] = form
    print(question_id)

    model_manager.answer(request, question_id)

    return render(request, 'question.html', context)


def tag(request, tag_name):
    context = model_manager.pagination(request, 'tag', tag_name=tag_name)
    return render(request, 'tag.html', context)


@login_required(login_url='login', redirect_field_name='continue')
def ask(request):
    form = model_manager.get_ask(request)
    if request.method == 'POST':
        if form.is_valid():
            q = form.save()
            q.created_time = timezone.now()
            q.author_id = request.user
            q.save()
            return redirect(reverse('question', kwargs={'question_id': q.id}))
    return render(request, "ask.html", context={'form': form})


def log_in(request):
    form = model_manager.get_login_form(request)
    if request.method == 'POST':
        user = authenticate(request, username=form['username'].value(), password=form['password'].value())
        if user is not None and form.is_valid():
            login(request, user)
            return redirect(reverse('index'))
        form.add_error('username', 'Username or Password is incorrect')
        form.add_error('password', 'Username or Password is incorrect')
    return render(request, "login.html", {'form': form})


def signup(request):
    form = model_manager.get_signup_form(request)
    if request.method == 'POST':
        print(form)
        if form.is_password_valid():
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect(reverse('index'))
        else:
            form.add_error('password', 'Пароли должны совпадать')
            form.add_error('repeat_password', 'Пароли должны совпадать')
    return render(request, "signup.html", context={'form': form})


def settings(request):
    return render(request, "settings.html")


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))
