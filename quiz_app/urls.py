from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('custom/', views.custom_question, name='custom_question'),
    path('quiz/', views.quiz, name='quiz'),
]
