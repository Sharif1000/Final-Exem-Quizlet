from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from quiz.models import QuizCategory, Quiz, Rating
from account.models import UserAccount
from quiz.forms import RatingForm
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.views import View
from django.utils.decorators import method_decorator

       
# Create your views here.
class HomepageView(ListView):
    model = Quiz
    template_name = 'home.html'
    context_object_name = 'quizes'

    def get_queryset(self):
        brand_slug = self.kwargs.get('Brand_Slug')
        if brand_slug:
            quizcategory = QuizCategory.objects.get(slug=brand_slug)
            queryset = Quiz.objects.filter(category=quizcategory).order_by('-average_rating')
        else:
            queryset = Quiz.objects.all().order_by('-average_rating')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = QuizCategory.objects.all()
        return context


def review(request,id):
    quiz_detail= Quiz.objects.get(id=id)
    quizreview=Rating.objects.filter(quiz=quiz_detail)
   
    if request.method=='POST':
        form=RatingForm(request.POST)
        if form.is_valid():
            try:    
                newReview=form.save(commit=False)
                newReview.quiz=quiz_detail
                newReview.reviewer = request.user.account
                newReview.save()
            except IntegrityError:
                messages.error(request, "You have already reviewed this quiz!")       
    else:
         form=RatingForm()
    return render(request,'reviews.html',{'form':form,'Reviews':quizreview})
