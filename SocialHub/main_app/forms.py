from django import forms

class UserForm(forms.Form):
    name = forms.CharField()
    passwd = forms.CharField()
