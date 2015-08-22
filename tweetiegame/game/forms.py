from django import forms


class GiveForm(forms.Form):
    giveword = forms.CharField(label='currentword', max_length=100, required=False, initial='')

class GuessForm(forms.Form):
    guessword = forms.CharField(label='guessword', max_length=100, required=False, initial='')