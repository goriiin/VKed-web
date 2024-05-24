from django import forms
from django.utils import timezone

from app.models import User, Profile, Question, Tag, Answer
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=4)

    def clean_username(self):
        try:
            username = self.cleaned_data.get('username')
            user = User.objects.get(username=username)
            return user
        except:
            raise ValidationError('There is no selected user')

    def save(self, **kwargs):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(widget=forms.PasswordInput, min_length=4, required=True)
    repeat_password = forms.CharField(widget=forms.PasswordInput, min_length=4, required=True)

    def clean(self):
        super(RegisterForm, self).clean()
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password != repeat_password:
            raise ValidationError('Passwords do not match')

    def is_password_valid(self):
        super(RegisterForm, self).clean()
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password != repeat_password:
            return False
        return True

    def is_user_valid(self, username):
        super(RegisterForm, self).clean()
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).count() > 0:
            return False

        if User.objects.filter(email=email).count() > 0:
            return False

    def save(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')

        if password != repeat_password:
            return ValidationError('Passwords do not match')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password)
        Profile.objects.create(user=user, avatar_path='static/img/default.jpg')


class AskForm(forms.Form):
    title = forms.CharField(min_length=3, max_length=30)
    description = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(required=True)

    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']

    def save(self):
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        tags = self.cleaned_data.get('tags').split(' ')
        date = timezone.now()
        question = Question.objects.create(title=title, content=description, created_time=date)
        for t in tags:
            try:
                question.tags.add(Tag.objects.get(tag_name=t))
            except:
                question.tags.add(Tag.objects.create(tag_name=t))
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Answer
        fields = ['description']

    def clean_text(self):
        super(AnswerForm, self).clean()
        text = self.cleaned_data.get('text')
        return text

    class Meta:
        model = Answer
        help_texts = {'text': 'Введите ответ'}

    def save(self):
        text = self.clean_text()
        ans = Answer.objects.create(answer=text, created_time=timezone.now())
        return ans
