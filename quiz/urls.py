from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quizdetail'),
]