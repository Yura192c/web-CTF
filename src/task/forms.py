from django import forms


class TaskAnswerForm(forms.Form):
    answer = forms.CharField(label='Ответ', max_length=200)
