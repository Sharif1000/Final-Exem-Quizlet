from django.db import models
from django.contrib.auth.models import User
from account.models import UserAccount
from django.core.validators import MinValueValidator, MaxValueValidator

class QuizCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length = 50, blank=True, null=True)
    def __str__(self):
        return self.name
    

class Quiz(models.Model):
    title= models.CharField(max_length=100)
    description= models.TextField()
    category = models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    has_time_limit = models.BooleanField(default=False)
    time_limit = models.PositiveIntegerField(blank=True, null=True)
    average_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)

    def get_questions(self):
        return self.question_set.all()
    
    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=300, null=True, blank=True)
    point_mark = models.PositiveIntegerField(null=True, blank=True)
    
    def get_answers(self):
        return self.answer_set.all()
    def __str__(self):
        return self.question_text
    
class Answer(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  answer_text = models.CharField(max_length=300, null=True, blank = True)
  is_correct = models.BooleanField(default=False)
  
  def __str__(self):
        return f'{self.answer_text} : {self.is_correct}'

class QuizAttempt(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user.user.username}: {self.quiz.title}'
    
class Rating(models.Model):
    reviewer = models.ForeignKey(UserAccount, on_delete = models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        blank=True,
        null=True
    )
    
    class Meta:
        unique_together = ['reviewer', 'quiz']
        
    def __str__(self):
        return f"Reviewer : {self.reviewer.user.first_name} ; Quiz {self.quiz.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_quiz_average_rating()

    def update_quiz_average_rating(self):
        ratings = Rating.objects.filter(quiz=self.quiz)
        total_ratings = ratings.count()
        if total_ratings > 0:
            total_rating = sum(rating.rating for rating in ratings if rating.rating is not None)
            average_rating = total_rating / total_ratings
            self.quiz.average_rating = round(average_rating, 2)
            self.quiz.save()
            
class UserProgress(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return f'User Progress: {self.score}'


