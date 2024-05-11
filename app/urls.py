
from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('ask', views.ask, name='ask'),
    path('signup', views.sign_up, name='signup'),
    path('login', views.log_in, name='login'),
    path('settings', views.settings, name='settings'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('logout', views.logout_view, name='logout'),
]

