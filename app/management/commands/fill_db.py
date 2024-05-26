from django.core.management.base import BaseCommand
from app.models import Profile, Question, Answer, Tag, AnswerLike, QuestionLike
from django.contrib.auth.models import User
import random
from django.utils import timezone
from faker import Faker
from app.models import QuestionLikeManager, AnswerLikeManager

fake = Faker()


class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio of data to generate')

    def handle(self, *args, **options):
        ratio = options['ratio']

        # Create users
        for i in range(ratio):
            user = User.objects.create_user((fake.user_name() + f"{i}"), (f"{i}" + fake.email()), '123')
            Profile.objects.create(user=user)

        # Create tags
        for i in range(ratio):
            name = fake.word()
            try:
                Tag.objects.create(tag_name=name)
            except:
                Tag.objects.create(tag_name=f'{name}_{fake.word()}')

        # Create questions
        for i in range(ratio * 10):
            profile = random.choice(Profile.objects.all())

            question = Question.objects.create(title=fake.sentence(), content=fake.paragraph(), author=profile)
            count = random.randint(1, 5)
            for _ in range(count):
                tag = random.choice(Tag.objects.all())
                question.tags.add(tag)

        # Create answers
        for i in range(ratio * 100):
            question = random.choice(Question.objects.all())
            profile = random.choice(Profile.objects.all())
            Answer.objects.create(answer=fake.paragraph(), question=question, author=profile, correct=fake.boolean())

        # Create question likes
        for i in range(ratio * 200):
            question = random.choice(Question.objects.all())
            profile = random.choice(Profile.objects.all())
            if not QuestionLike.objects.filter(user_id=profile, question_id=question).exists():
                QuestionLike.objects.add_vote(user_id=profile, question_id=question, vote=fake.boolean())

        # Create answer likes
        for i in range(ratio * 200):
            answer = random.choice(Answer.objects.all())
            profile = random.choice(Profile.objects.all())
            if not AnswerLike.objects.filter(user_id=profile, answer_id=answer.id).exists():
                AnswerLike.objects.add_vote(user_id=profile, answer_id=answer.id, vote=fake.boolean())

        self.stdout.write(self.style.SUCCESS(f'Database filled with {ratio}x data'))
