from polls.models import *
from django.forms import ModelForm, ModelChoiceField, Form, CharField


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']


class ChoiceForm(Form):
    choice_text = CharField(required=False, label='Choice text name', max_length=500)