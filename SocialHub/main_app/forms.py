from django import forms

class UserForm(forms.Form):
    name = forms.CharField()
    passwd = forms.CharField()

class FacebookUserForm(UserForm):
    pass

class TwitterUserForm(UserForm):
    pass
