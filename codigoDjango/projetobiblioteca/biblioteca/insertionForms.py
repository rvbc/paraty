from django import forms
import datetime

class SuggestionForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    
    title = forms.CharField(max_length=100)
    writer = forms.CharField(max_length=100)

    publisher = forms.CharField(max_length=100)
    year = forms.IntegerField(min_value=1, max_value=datetime.datetime.now().year)
    edition = forms.IntegerField(min_value=1)
