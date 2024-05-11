from django.contrib.auth import authenticate, login
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from app import model_manager
from django.urls import reverse

def index(request):
    context = model_manager.pagination(request, 'index')
    print(context)
    return render(request, 'index.html', context)


def hot(request):
    context = model_manager.pagination(request, 'hot')
    return render(request, 'hot.html', context)


def question(request, question_id):
    context = model_manager.this_question(request, question_id)
    if context['page'] == -1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'question.html', context)


def tag(request, tag_name):
    context = model_manager.pagination(request, 'tag', tag_name=tag_name)
    return render(request, 'tag.html', context)


def ask(request):
    return render(request, "ask.html")


def log_in(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        return redirect(reverse('index'))
    return render(request, "login.html")


def sign_up(request):
    return render(request, "signup.html")


def settings(request):
    return render(request, "settings.html")


def logout_view(request):
    return redirect("/login")
