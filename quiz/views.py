from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Quiz, Question, QuizAttempt, Answer
from .forms import QuizAttemptForm
from django.http import HttpResponse, HttpRequest
from django.db.models import Count
from django.core.paginator import Paginator
from typing import Optional
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth import get_user

# Create your views here.
def send_quiz_email(user, score, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'score' : score,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    if request.method == 'POST':
        form = QuizAttemptForm(request.POST, quiz=quiz)
        if form.is_valid():
            score = 0
            for question in questions:
                selected_option = form.cleaned_data.get(f'question_{question.id}')
                if selected_option == 'True':
                    score += 1
            
            user_account = request.user.account
            quiz_attempt = form.save(commit=False)
            quiz_attempt.user = user_account
            quiz_attempt.quiz = quiz
            quiz_attempt.score = score
            quiz_attempt.end_time = timezone.now()
            quiz_attempt.save()
            messages.success(request, f'Quiz submitted successfully! Your score: {score}')
            send_quiz_email(request.user, score, "Quiz Mark Message", "quiz_mark_email.html")
            return redirect('profile')
    else:
        form = QuizAttemptForm(quiz=quiz)
    return render(request, 'quiz_detail.html', {'quiz': quiz, 'questions': questions, 'form': form})