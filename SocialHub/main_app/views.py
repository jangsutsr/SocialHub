from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, FacebookUserForm, TwitterUserForm
from .models import UserProfile

@require_http_methods(['POST'])
def register(request):
    form = UserForm(request.POST)
    if form.is_valid():
        try:
            user = User.objects.create_user(form['name'].data,
                                            password=form['passwd'].data)
            UserProfile.create_profile(user)
            return HttpResponse('Successfully create user.')
        except IntegrityError:
            return HttpResponse('User name exists.')
    else:
        return HttpResponse('Invalid input data')

@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.method == 'GET':
        return HttpResponse('Indicator that redirection to login page is needed.')
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form['name'].data,
                                password=form['passwd'].data)
            if user != None:
                login(request, user)
                return HttpResponse('User exists.')
            else:
                return HttpResponse('User does not exist.')
        else:
            return HttpResponse('Invalid input data')

@require_http_methods(['GET'])
@login_required
def log_out(request):
    logout(request)
    return HttpResponse('Session deleted')

@require_http_methods(['POST'])
@login_required
def attach(request, app_name):
    if app_name == 'facebook':
        form = FacebookUserForm(request.POST)
        if form.is_valid():
            UserProfile.insert_account(form, request.user, 1)
            return HttpResponse('facebook account attached')
        else:
            return HttpResponse('Invalid input data')
    elif app_name == 'twitter':
        form = TwitterUserForm(request.POST)
        if form.is_valid():
            UserProfile.insert_account(form, request.user, 2)
            return HttpResponse('twitter account attached')
        else:
            return HttpResponse('Invalid input data')
    else:
        return HttpResponse('Unsupported social network')

def show_twitters(request):
    pass
