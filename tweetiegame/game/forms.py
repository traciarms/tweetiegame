from django import forms


class WordsForm(forms.Form):
    currentword = forms.CharField(label='currentword', max_length=100, required=False)
    guessword = forms.CharField(label='guessword', max_length=100, required=False)