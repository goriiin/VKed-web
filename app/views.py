from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from app import model_manager

# Create your views here.

QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore "
                f"et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut ",
        "tags": ["tag1", "tag2", "tag3"],
    } for i in range(200)
]

ANSWERS = [
    {
        "text": f"{i} Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porttitor est diam, "
                f"vel pellentesque sapien molestie non. Suspendisse pretium augue."
    } for i in range(20)
]


def index(request):
    context = model_manager.pagination(request, 'index')
    if context['page'] == -1:
        return HttpResponseNotFound('404 Error')
    return render(request, 'index.html', context)


def hot(request):
    context = model_manager.pagination(request, 'hot')
    if context['page'] == -1:
        return HttpResponseNotFound('404 Error')
    return render(request, 'hot.html', context)


def question(request, question_id):
    context = model_manager.this_question(request, question_id)
    if context['page'] == -1:
        return HttpResponseNotFound('Bad request')
    context['form'] = settings.give_answer(request, question_id)
    return render(request, 'question.html', context)


def tag(request, tag_name):
    context = model_manager.pagination(request, 'tag', tag_name=tag_name)
    if context['page'] == -1:
        return HttpResponseNotFound('404 Error')
    return render(request, 'tag.html', context)


def ask(request):
    return render(request, "ask.html")


def login(request):
    return render(request, "login.html")


def sign_up(request):
    return render(request, "signup.html")


def settings(request):
    return render(request, "settings.html")


def logout_view(request):
    return redirect("/login")
