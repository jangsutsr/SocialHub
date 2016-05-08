from django import forms

class UserForm(forms.Form):
    name = forms.CharField()
    passwd = forms.CharField()

class FacebookUserForm(forms.Form):
    name = forms.CharField()
    token = forms.CharField()
    identity = forms.CharField()

class TwitterUserForm(forms.Form):
    name = forms.CharField()
    identity = forms.CharField()
    key = forms.CharField()
    secret = forms.CharField()
