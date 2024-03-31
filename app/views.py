from django.shortcuts import render

# Create your views here.

QUESTION = [
    {
        "title": f"Question {i}",
        "text": f"This is the {i} question",
    } for i in range(10)
]


def index(request):
    return render(request, "index.html", {"questions": QUESTION})

