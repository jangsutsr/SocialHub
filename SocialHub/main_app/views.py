# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info, success, error, get_messages
from json import dumps
from .forms import UserForm, FacebookUserForm, TwitterUserForm
from .models import UserProfile, Message
from SocialHub.utils import wav_to_mp3

@require_http_methods(['POST'])
def register(request):
    form = UserForm(request.POST)
    if form.is_valid():
        try:
            user = User.objects.create_user(form['name'].data,
                                            password=form['passwd'].data)
            #UserProfile.create_profile(user)
            success(request, 'Successfully create user.')
        except IntegrityError:
            error(request, 'User name exists.')
    else:
        error(request, 'Invalid input data')
    return HttpResponse(''.join([item.message for item in get_messages(request)]))

@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.method == 'GET':
        info(request, 'Indicator')
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form['name'].data,
                                password=form['passwd'].data)
            if user != None:
                login(request, user)
                success(request, 'User exists.')
            else:
                error(request, 'User does not exist.')
        else:
            error(request, 'Invalid input data')
    return HttpResponse(''.join([item.message for item in get_messages(request)]))

@require_http_methods(['GET'])
@login_required
def log_out(request):
    logout(request)
    info(request, 'Session deleted')
    return HttpResponse(''.join([item.message for item in get_messages(request)]))

@require_http_methods(['POST'])
@login_required
def attach(request, app_name):
    if app_name == 'facebook':
        form = FacebookUserForm(request.POST)
        if form.is_valid():
            UserProfile.insert_account(form, request.user, 1)
            success(request, 'facebook account attached')
        else:
            error(request, 'Invalid input data')
    elif app_name == 'twitter':
        form = TwitterUserForm(request.POST)
        if form.is_valid():
            UserProfile.insert_account(form, request.user, 2)
            success(request, 'twitter account attached')
        else:
            error(request, 'Invalid input data')
    else:
        error(request, 'Unsupported social network')
    return HttpResponse(''.join([item.message for item in get_messages(request)]))

@require_http_methods(['GET'])
@login_required
def show(request):
    msg_list = Message.get_posts(request.user)
    UserProfile.update_query_time(request.user)
    for i in range(len(msg_list)):
        msg_list[i]['time'] = msg_list[i]['time'].strftime('%a %b %d %H:%M:%S +0000 %Y')
    return JsonResponse(msg_list,
                        safe=False,
                        json_dumps_params={'indent': 2,
                                           'ensure_ascii': False})

@require_http_methods(['GET'])
@login_required
def history(request, offset):
    msg_list = Message.get_offset_posts(request.user, int(offset))
    for i in range(len(msg_list)):
        msg_list[i]['time'] = msg_list[i]['time'].strftime('%a %b %d %H:%M:%S +0000 %Y')
    return JsonResponse(msg_list,
                        safe=False,
                        json_dumps_params={'indent': 2,
                                           'ensure_ascii': False})

@require_http_methods(['GET'])
def audio(request):
    from requests.auth import HTTPBasicAuth
    from requests import post

    tts_usersame = '32af5fd9-24ba-4b27-bd3d-638e194cc682'
    tts_password = 'zDyYeYhU2mUe'
    tts_auth=HTTPBasicAuth(tts_usersame, tts_password)

    tts_url = 'https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize'
    tts_headers = {'Content-Type': 'application/json', 'Accept': 'audio/wav'}
    text = request.GET['data']
    data = post(tts_url, auth=tts_auth, headers=tts_headers, data=dumps({'text': text}))
    response = HttpResponse(wav_to_mp3(data.content), content_type='audio/mp3')
    response['Content-Disposition'] = 'attachment; filename="test.mp3"'
    return response
