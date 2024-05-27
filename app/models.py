from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone


# =================Tag============================== #

class TagQuerySet(models.QuerySet):
    def is_tag(self, tag):
        return self.filter(tag_name=tag)

    def increment_used_times(self, tag_ids):
        self.filter(id__in=tag_ids).update(used_times=models.F('used_times') + 1)


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def is_tag(self, tag):
        return self.get_queryset().is_tag(tag)


class Tag(models.Model):
    tag_name = models.CharField(max_length=32, unique=True)
    used_times = models.PositiveIntegerField(default=0)

    objects = TagManager()

    def __str__(self):
        return self.tag_name


# =================Profile============================== #

class ProfileQuerySet(models.QuerySet):
    def is_profile(self, profile):
        return self.filter(user__username=profile)

    def increment_answers_count(self, profile_id):
        self.filter(id=profile_id).update(answers_count=(models.F('answers_count') + 1))


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def is_profile(self, profile):
        return self.get_queryset().is_profile(profile)


class Profile(models.Model):
    updated_time = models.DateTimeField(auto_now=True)
    avatar_path = models.ImageField(upload_to='images', default='default.jpg')
    answers_count = models.PositiveIntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    def __int__(self):
        return self.pk


# ============Question=================================== #

class QuestionQueryset(models.QuerySet):
    def order_rating(self):
        return self.order_by('-created_time').order_by('-likes_count')

    def order_time(self):
        return self.order_by('-created_time')

    def tags(self, tag_name):
        return self.filter(tags__tag_name=tag_name).order_by('created_time')

    def get_tags(self):
        return [tag.tag_name for tag in self.tags.all()]

    def increment_answers_count(self, question_id):
        # Увеличиваем счетчик ответов для вопроса
        self.filter(id=question_id).update(answers_count=models.F('answers_count') + 1)


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQueryset(self.model, using=self._db)

    def hot(self):
        return self.get_queryset().order_rating()

    def news(self):
        return self.get_queryset().order_time()

    def get_tags(self):
        return self.get_queryset().get_tags()


class Question(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(default=timezone.now)
    likes_count = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)

    tags = models.ManyToManyField(Tag, related_name='questions')

    objects = QuestionManager()

    def __int__(self):
        return self.pk

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.pk:
            Tag.objects.get_queryset().increment_used_times(self.tags.values_list('id', flat=True))


# ===============QuestionLike================================ #

class QuestionLikeQuerySet(models.QuerySet):
    def add_vote(self, user_id, question_id, vote):
        q = Question.objects.get(pk=question_id)
        try:
            self.create(user_id=user_id, question_id=question_id, vote=vote)
            q.likes_count += vote
            q.save()
            return q.likes_count

        except:
            item = QuestionLike.objects.get_queryset().get(user_id=user_id, question_id=question_id)
            if item.vote != vote:
                q.likes_count += vote
                item.vote = vote
                item.save()
                q.save()
            else:
                item.vote = 0
                item.save()
                q.likes_count = QuestionLike.objects.filter(question_id=q.id).aggregate(Sum('vote'))['vote__sum']
                q.save()


class QuestionLikeManager(models.Manager):
    def get_queryset(self):
        return QuestionLikeQuerySet(self.model, using=self._db)

    def add_vote(self, user_id, question_id, vote):
        self.get_queryset().add_vote(user_id=user_id, question_id=question_id, vote=vote)


class QuestionLike(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = models.IntegerField()

    objects = QuestionLikeManager()

    class Meta:
        unique_together = (('question_id', 'user_id'),)


# =============Answer================================== #

class AnswerQuerySet(models.QuerySet):
    def hots(self):
        return self.order_by('-likes_count')


class AnswerManager(models.Manager):
    def get_queryset(self):
        return AnswerQuerySet(self.model, using=self._db)

    def hots(self):
        return self.get_queryset().hots()


class Answer(models.Model):
    objects = AnswerManager()
    answer = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    correct = models.BooleanField(default=False, null=False)

    likes_count = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.answer

    def __int__(self):
        return self.pk

    def save(self, *args, **kwargs):
        created = self._state.adding

        super().save(*args, **kwargs)

        if created:
            if self.question:
                self.question.answers_count += 1
                self.question.save()
            if self.author:
                self.author.answers_count += 1
                self.author.save()


# =============AnsweLiker================================== #

class AnswerLikeQuerySet(models.QuerySet):
    def add_vote(self, user_id, answer_id, vote):
        a = Answer.objects.get(pk=answer_id)
        try:
            item = self.create(user_id=user_id, answer_id=answer_id, vote=vote)
            a.likes_count += vote
            a.save()
            item.save()
        except:
            item = AnswerLike.objects.get_queryset().get(user_id=user_id, answer_id=answer_id)
            if item.vote != vote:
                item.vote = vote
                item.save()

                a.likes_count = AnswerLike.objects.filter(answer_id=a.id).aggregate(Sum('vote'))['vote__sum']
                a.save()
            else:
                item.vote = 0
                item.save()
                a.likes_count = AnswerLike.objects.filter(answer_id=a.id).aggregate(Sum('vote'))['vote__sum']
                a.save()


class AnswerLikeManager(models.Manager):
    def get_queryset(self):
        return AnswerLikeQuerySet(self.model, using=self._db)

    def add_vote(self, user_id, answer_id, vote):
        self.get_queryset().add_vote(user_id=user_id, answer_id=answer_id, vote=vote)


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    vote = models.IntegerField()
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

    objects = AnswerLikeManager()

    class Meta:
        unique_together = ('user_id', 'answer')
