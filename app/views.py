from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.

QUESTIONS = [
    {
        "title": f"Question {i}",
        "text": f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore "
                f"et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut "
                f"aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse "
                f"cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, "
                f"sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "tags": ["tag1", "tag2", "tag3"],
    } for i in range(200)
]

ANSWERS = [
    {
        "text": f"{i} Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porttitor est diam, "
                f"vel pellentesque sapien molestie non. Suspendisse pretium augue."
    } for i in range(2)
]


def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5)
    page_obj = paginator.page(page_num)

    return render(request, "index.html", {"questions": QUESTIONS})


def hot(request):
    return render(request, "hot.html", {"questions": QUESTIONS[::-1]})


def questions(request, question_id):
    item = QUESTION[question_id]
    return render(request, "question.html", {"question": item, "answers": ANSWERS})


def ask(request):
    return render(request, "ask.html")


def login(request):
    return render(request, "login.html")


def sign_up(request):
    return render(request, "signup.html")


def tag(request, tag_name):
    for q in QUESTION:
        q["tags"] = [tag_name]
    return render(request, "tag.html", {"tag_name": tag_name, "questions": QUESTIONS[::4]})


def settings(request):
    return render(request, "settings.html")


def logout(request):
    return redirect("/login", permanent=True)

def pagination():
    pass