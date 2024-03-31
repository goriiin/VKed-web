from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.

QUESTIONS = [
    {
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


def pagination(request, items, count=3):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(items, count)
    page_obj = paginator.get_page(page_num)
    return paginator, page_obj, page_num


def index(request):
    paginator, questions, page_num = pagination(request, QUESTIONS)
    return render(request, "index.html", {"questions": questions, "paginator": paginator})


def hot(request):
    paginator, items, page_num = pagination(request, QUESTIONS)
    return render(request, "hot.html", {"items": items[::-1], "paginator": paginator})


def question(request, question_id):
    item = QUESTIONS[question_id]
    paginator, items, page_num = pagination(request, ANSWERS, 2)
    return render(request, "question.html", {"question": item, "answers": items, "paginator": pagination(request, ANSWERS, 2)})


def ask(request):
    return render(request, "ask.html")


def login(request):
    return render(request, "login.html")


def sign_up(request):
    return render(request, "signup.html")


def tag(request, tag_name):
    Q = QUESTIONS.copy()
    for q in Q:
        q["tags"] = [tag_name]
    paginator, items, page_num = pagination(request, QUESTIONS)
    return render(request, "index.html", {"items": items, "paginator": paginator})


def settings(request):
    return render(request, "settings.html")


def logout_view(request):
    logout(request)
    return redirect("/login", permanent=True)
