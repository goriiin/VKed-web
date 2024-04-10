from django.core.paginator import Paginator
from django.shortcuts import render, redirect

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
    paginator, questions, page_num = pagination(request, QUESTIONS)

    return render(request, "index.html", {"questions": questions, "paginator": paginator})


def hot(request):
    paginator, questions, page_num = pagination(request, QUESTIONS[::-1])
    return render(request, "index.html", {"questions": questions, "paginator": paginator})


def question(request, question_id):
    item = QUESTIONS[question_id]
    paginator, items, page_num = pagination(request, ANSWERS, 2)
    return render(request, "question.html",
                  {"question": item, "answers": items, "paginator": pagination(request, ANSWERS, 2)})


def ask(request):
    return render(request, "ask.html")


def login(request):
    return render(request, "login.html")


def sign_up(request):
    return render(request, "signup.html")


def tag(request, tag_name):
    Q = QUESTIONS.copy()
    print(tag_name)
    for q in Q:
        q["tags"] = [tag_name]
    paginator, questions, page_num = pagination(request, Q)
    return render(request, "tag.html", {"tag": tag_name, "questions": questions, "paginator": paginator})


def settings(request):
    return render(request, "settings.html")


def logout_view(request):
    return redirect("/login")
