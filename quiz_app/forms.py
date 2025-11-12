
from django import forms

class CustomQuestionForm(forms.Form):
    theme_name = forms.CharField(label="Nom du thème")
    question_text = forms.CharField(label="Question")
    option_a = forms.CharField(label="Option A")
    option_b = forms.CharField(label="Option B")
    option_c = forms.CharField(label="Option C")
    option_d = forms.CharField(label="Option D")
    correct_answer = forms.ChoiceField(choices=[('A','A'),('B','B'),('C','C'),('D','D')])