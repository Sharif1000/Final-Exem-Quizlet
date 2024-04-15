from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import FormView
from .forms import UserRegistrationForm
from quiz.models import QuizAttempt, Quiz
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from account.models import UserAccount
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('homepage')
    
    def form_valid(self, form):
        user = form.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f"http://127.0.0.1:8000/account/active/{uid}/{token}"
        email_subject = "Confirm Your Email"
        email_body = render_to_string('accounts/confirm_email.html', {'confirm_link' : confirm_link})
        
        email = EmailMultiAlternatives(email_subject , '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        messages.success(self.request, "Check your mail for confirmation.")
        return redirect("login")
    
    def form_invalid(self, form):
        error_dict = form.errors.as_data()
        if error_dict:
            error_message = error_dict.popitem()[1][0].message
            messages.error(self.request, error_message)
        return super().form_invalid(form)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('homepage')

def user_logout(request):
    logout(request)
    return redirect('homepage')

@login_required
def profile(request):
    account_instance = UserAccount.objects.get(user=request.user)
    quiz_attempt= QuizAttempt.objects.filter(user=account_instance)
    return render(request, 'accounts/profile.html', {'lists':quiz_attempt})

@login_required
def leaderboad(request):
    quiz_attempt= QuizAttempt.objects.all().order_by('-score')[:10]
    enumerated_quiz_attempt = list(enumerate(quiz_attempt, start=1))
    return render(request, 'accounts/leaderboad.html', {'enumerated_lists': enumerated_quiz_attempt})

@login_required
def quizleaderboard(request, id):
    quiz_detail= Quiz.objects.get(id=id)
    quiz_attempt= QuizAttempt.objects.filter(quiz=quiz_detail).order_by('-score')
    enumerated_quiz_attempt = list(enumerate(quiz_attempt, start=1))
    return render(request, 'accounts/quizleaderboad.html', {'enumerated_lists': enumerated_quiz_attempt})