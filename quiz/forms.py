from django import forms
from .models import Rating, QuizAttempt, Question
        
class RatingForm(forms.ModelForm):
    class Meta: 
        model = Rating
        fields = ['body', 'rating']
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })



class QuizAttemptForm(forms.ModelForm):
    class Meta:
        model = QuizAttempt
        fields = []

    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz', None)
        super().__init__(*args, **kwargs)
        if quiz:
            questions = quiz.question_set.all()
            for question in questions:
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.question_text,
                    choices=[(answer.is_correct, answer.answer_text) for answer in question.answer_set.all()],
                    widget=forms.RadioSelect(),
                    required=False
                )

    