from django import forms



css_attributes = {
    "class" : "form-control"
    }

class Loginform(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs= {
        **css_attributes,"id" : "userName","placeholder" : "Enter your username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs= {
        **css_attributes,"id" : "password","placeholder" : "Enter your password"}))


class Signupform(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        **css_attributes,"id":"email","placeholder":"Enter the email id"}))
    confirm_password = forms.CharField()