from django import forms

class Userform(forms.Form):
    name = forms.CharField(max_length=100)