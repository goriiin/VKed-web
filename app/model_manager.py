from django.core.paginator import Paginator

from app.models import Question, Tag


def index(page, count):
    return Question.objects.news()[(page - 1) * count: page * count]


def hot(page, count):
    return Question.objects.hot()[(page - 1) * count: page * count]


def tag(page, count, tag_name):
    return Tag.objects.is_tag(tag_name)[(page - 1) * count: page * count]


def check_page(request):
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            return -1
    except:
        return -1

    return page


def pages(page, count):
    if count <= 1:
        return []
    if count < 5:
        return [i for i in range(1, count + 1)]
    if 4 < page < count:
        return [1, '...'] + [i for i in range(page - 2, page + 3)] + ['...', count]
    elif page > 4:
        return [1, '..'] + [i for i in range(page - 2, count + 1)]
    return [i for i in range(1, page + 3)] + ['...', count]


def pagination(request, type_req, count=3, tag_name=None):
    page_num = check_page(request)
    if page_num == -1:
        return {'page_num': -1}

    if type_req == 'index':
        items = index(page_num, count)
    elif type_req == 'hot':
        items = hot(page_num, count)
    else:
        items = tag(page_num, count, tag_name)

    paginator = Paginator(items, count)
    page_obj = paginator.get_page(page_num)
    return paginator, page_obj, page_num


def this_question(request, question_id, count=5):
    page = check_page(request)
    if page == -1:
        return {'page': -1}
    try:
        question = Question.objects.get(pk=question_id)
    except:
        return {'page': -1}

    tags = question.tags.all()
    answers = question.answer_set.all()[(page - 1) * count: page * count]

    return {
        'page': page, 'question': question, 'tags': tags, 'answers': answers,
        'pages': pages(page, (question.answer_set.count() + count - 1))
    }
