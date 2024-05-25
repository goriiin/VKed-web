from django.core.management.base import BaseCommand
from app.models import Profile, Question, Answer, Tag, AnswerLike, QuestionLike
from django.contrib.auth.models import User
import random
from django.utils import timezone
from faker import Faker
from PIL import Image
import os

fake = Faker()

class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio of data to generate')

    def handle(self, *args, **options):
        ratio = options['ratio']

        # Create users
        users = []
        for i in range(ratio):
            user = User.objects.create_user((fake.user_name() + f"{i}"), (f"{i}" + fake.email()), '123')
            avatar_file = f"avatar_{i}.jpg"
            avatar_path = os.path.join("avatars", avatar_file)
            image = Image.new('RGB', (100, 100))
            image.save(avatar_file)
            profile = Profile.objects.create(user=user, avatar=avatar_path)
            users.append(profile)

        # Create tags
        tags = []
        for i in range(ratio):
            tag = Tag.objects.create(tag_name=(fake.word() + f"{i}"))
            tags.append(tag)

        # Create questions
        questions = []
        for i in range(ratio * 10):
            user = random.choice(users)
            tag = random.choice(tags)
            question = Question.objects.create(title=fake.sentence(), content=fake.paragraph(), author=user)
            question.tags.add(tag)
            questions.append(question)

        # Create answers
        answers = []
        for i in range(ratio * 100):
            question = random.choice(questions)
            user = random.choice(users)
            answer = Answer.objects.create(answer=fake.paragraph(), question=question, author=user)
            answers.append(answer)

        # Create question likes
        for i in range(ratio * 200):
            question = random.choice(questions)
            user = random.choice(users)
            if not QuestionLike.objects.filter(user_id=user, question_id=question).exists():
                QuestionLike.objects.create(user_id=user, question_id=question, vote=fake.boolean())

        # Create answer likes
        for i in range(ratio * 200):
            answer = random.choice(answers)
            user = random.choice(users)
            if not AnswerLike.objects.filter(user_id=user, answer_id=answer).exists():
                AnswerLike.objects.create(user_id=user, answer_id=answer, vote=fake.boolean())

        self.stdout.write(self.style.SUCCESS(f'Database filled with {ratio}x data'))