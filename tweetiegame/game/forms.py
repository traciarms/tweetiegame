from django import forms


class WordForm(forms.Form):
    word = forms.CharField(label='word', max_length=100,)
