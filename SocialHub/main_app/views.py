from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from .forms import UserForm, FacebookUserForm, TwitterUserForm
from .models import User, UserRecord

@require_http_methods(['POST'])
def register(request):
    form = UserForm(request.POST)
    if form.is_valid():
        if User.insert_user(form):
            return HttpResponse('Successfully create user.')
        else:
            return HttpResponse('User name exists.')
    else:
        return HttpResponse('Invalid input data')

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        return HttpResponse('Indicator that redirection to login page is needed.')
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            if User.does_exist(form):
                request.session['user'] = form['name'].data
                return HttpResponse('User exists.')
            else:
                return HttpResponse('User does not exist.')
        else:
            return HttpResponse('Invalid input data')

@require_http_methods(['GET'])
def logout(request):
    request.session.pop('user')
    return HttpResponse('Session deleted')

@require_http_methods(['POST'])
def attach(request, app_name):
    if app_name == 'facebook':
        form = FacebookUserForm(request.POST)
        if form.is_valid():
            obj = UserRecord.insert_user(form, 1)
            User.attach_account(obj, request.session['user'], 1)
            return HttpResponse('facebook account attached')
        else:
            return HttpResponse('Invalid input data')
    elif app_name == 'twitter':
        form = TwitterUserForm(request.POST)
        if form.is_valid():
            obj = UserRecord.insert_user(form, 2)
            User.attach_account(obj, request.session['user'], 2)
            return HttpResponse('twitter account attached')
        else:
            return HttpResponse('Invalid input data')
    else:
        return HttpResponse('Unsupported social network')

def show_twitters(request):
    pass
