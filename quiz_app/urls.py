from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('custom/', views.custom_question, name='custom_question'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz_review_all/', views.quiz_review_all, name='quiz_review_all'),
    path('restart/', views.restart_quiz, name='restart_quiz'),
]
