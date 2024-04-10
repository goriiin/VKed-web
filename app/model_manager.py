from django.core.paginator import Paginator

from app.models import Question, Tag


def index():
    return Question.objects.news()


def hot():
    return Question.objects.hot()


def tag(tag_name):
    return Tag.objects.is_tag(tag_name)


def check_page(request):
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            return -1
    except:
        return -1

    return page


def pagination(request, type_req, count=4, tag_name=None):
    page_num = check_page(request)
    if page_num == -1:
        return {'page_num': -1}

    if type_req == 'index':
        items = index(page_num, count)
    elif type_req == 'hot':
        items = hot(page_num, count)
    elif type_req == 'question':
        items = tag(page_num, count, tag_name)

    paginator = Paginator(items, count)
    items = paginator.get_page(page_num)

    return {'questions': items,
            'paginator': paginator}


def this_question(request, question_id, count=4):
    page_num = check_page(request)
    if page_num == -1:
        return {'page': -1}
    try:
        question = Question.objects.get(pk=question_id)
    except:
        return {'page': -1}

    tags = question.tags.all()
    answers = question.answer_set.all()

    paginator = Paginator(answers, count)
    answers = paginator.get_page(page_num)

    return {
        'question': question, 'tags': tags, 'answers': answers,
        'paginator': paginator
    }
