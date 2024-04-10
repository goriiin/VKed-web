from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# =================Tag============================== #

class TagQuerySet(models.QuerySet):
    def is_tag(self, tag):
        return self.filter(tag_name=tag)


class TagManager(models.Manager):
    def is_tag(self, tag):
        return self.get_queryset().is_tag(tag)


class Tag(models.Model):
    tag_name = models.CharField(max_length=32, unique=True)

    objects = TagManager()

    def __str__(self):
        return self.tag_name


# =================Profile============================== #


class Profile(models.Model):
    updated_time = models.DateTimeField(auto_now=True)
    avatar_path = models.ImageField(null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.user.name


# ============Question=================================== #


class QuestionQueryset(models.QuerySet):
    def order_rating(self):
        return self.order_by('-likes_count')

    def order_time(self):
        return self.order_by('-created_date')


class QuestionManager(models.Manager):
    def hot(self):
        return self.get_queryset().order_rating()

    def news(self):
        return self.get_queryset().order_time()


class Question(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    created_time = models.DateTimeField(default=timezone.now())
    objects = QuestionManager()

    likes_count = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)


# ===============QuestionLike================================ #


class QuestionLikeQuerySet(models.QuerySet):
    def add_vote(self, user_id, question_id, vote):
        q = Answer.objects.get(pk=question_id)
        try:
            self.create(user_id=user_id, question_id=question_id, rating=vote)
            q.likes_count += vote

        except:
            item = self.get(user_id=user_id, question_id=question_id)
            q.likes_count -= item.rating
            q.likes_count += vote
            item.rating = vote

            item.save()
        q.save()


class QuestionLikeManager(models.Manager):
    def add_vote(self, user_id, question_id, vote):
        self.get_queryset().add_vote(user_id=user_id, question_id=question_id, vote=vote)


class QuestionLike(models.Model):
    user_id = models.OneToOneField(Profile, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = QuestionLikeManager()

    class Meta:
        unique_together = (('question_id', 'user_id'),)


# =============Answer================================== #

class AnswerQuerySet(models.QuerySet):
    def hots(self):
        return self.order_by('-likes_count')


class AnswerManager(models.Manager):
    def hots(self):
        return self.get_queryset().hots()


class Answer(models.Model):
    objects = AnswerManager
    answer = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    likes_count = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.answer


# =============AnsweLiker================================== #


class AnswerLikeQuerySet(models.QuerySet):
    def add_vote(self, user_id, answer_id, vote):
        a = Answer.objects.get(pk=answer_id)
        try:
            self.create(user_id=user_id, answer_id=answer_id, rating=vote)
            a.likes_count += vote

        except:
            item = self.get(user_id=user_id, answer_id=answer_id)
            a.likes_count -= item.rating
            a.likes_count += vote
            item.rating = vote

            item.save()
        a.save()


class AnswerLikeManager(models.Manager):
    def add_vote(self, user_id, question_id, vote):
        self.get_queryset().add_vote(user_id=user_id, question_id=question_id, vote=vote)


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    user_id = models.OneToOneField(Profile, on_delete=models.CASCADE)

    objects = AnswerLikeManager

    class Meta:
        unique_together = ('user_id', 'answer')
