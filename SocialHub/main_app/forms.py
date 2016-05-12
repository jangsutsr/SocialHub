from django import forms

class UserForm(forms.Form):
    '''Form used for validating user info.

    This form is used in both registration and login authentication.
    '''
    name = forms.CharField()
    passwd = forms.CharField()
