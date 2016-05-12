# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info, success, error, get_messages
from django.http import QueryDict

import requests
from requests_oauthlib import OAuth1
from json import dumps, loads
from threading import Thread
from .forms import UserForm
from .models import UserProfile, Message, Friend
from util import wav_to_mp3
from util.social_init import social_init

client_key = '1VjKOBZr4k8cRycT05PNyXj2i'
client_secret = 'QIIfKQjaGYdBZB1jL1lzGRgNFXCfk87AyyLr8uliHuPLFsYKSo'

@require_http_methods(['POST'])
def register(request):
    '''View function handling user registration.

    This function parse and validate incoming request's form data and check
    table auth_user for authenticity before storing user record in table or
    output error message.

    Args:
        request: Incoming request.

    Returns:
        Indicator that user is successfully created or error message that either
        form data is invalid or user exists.
    '''
    form = UserForm(request.POST)
    response = HttpResponse()
    if form.is_valid():
        try:
            user = User.objects.create_user(form.cleaned_data['name'],
                                            password=form.cleaned_data['passwd'])
            success(request, 'Successfully create user.')
        except IntegrityError:
            error(request, 'User name exists.')
            response.status_code = 400
    else:
        error(request, 'Invalid input data')
        response.status_code = 400
    response.write(''.join([item.message for item in get_messages(request)]))
    return response

@require_http_methods(['GET', 'POST'])
def log_in(request):
    '''View function corresponding to url /login.

    The purpose of this function vary with http method. If method is GET it
    behaves as unauthorize redirect destination; If method is POST it accepts
    request's form data, validates it and adds session to authorize the user.

    Args:
        request: Incoming request

    Returns:
        When GET, indicate the page has been redirected here; When POST,
        return either message that user is logged in or error that form invalid
        or user name/password error.
    '''
    response = HttpResponse()
    if request.method == 'GET':
        info(request, 'Indicator')
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['name'],
                                password=form.cleaned_data['passwd'])
            if user != None:
                login(request, user)
                success(request, 'User exists.')
            else:
                error(request, 'User does not exist.')
                response.status_code = 400
        else:
            error(request, 'Invalid input data')
            response.status_code = 400
    response.write(''.join([item.message for item in get_messages(request)]))
    return response

@require_http_methods(['GET'])
@login_required
def log_out(request):
    '''View function to log user out.

    This function delete related session to log user out.

    Args:
        request: Incoming request.

    Returns:
        Message that user is successfully logged out.
    '''
    logout(request)
    info(request, 'Session deleted')
    return HttpResponse(''.join([item.message for item in get_messages(request)]))

@require_http_methods(['GET'])
@login_required
def attach(request, app_name):
    '''View function to attach facebook/twitter account to user.

    If a twitter account is to be attached, the incoming request is simply an
    indicator. This function then call twitter request_token api to ask for a
    temporary
    '''
    response = HttpResponse()
    if app_name == 'facebook':
        success(request, 'facebook account attached')
    elif app_name == 'twitter':
        request_token_url = 'https://api.twitter.com/oauth/request_token'
        oauth = OAuth1(client_key,
                       client_secret=client_secret)
        r = requests.post(url=request_token_url,
                          auth=oauth,
                          data={'oauth_callback': 'http://ec2-54-173-9-169.compute-1.amazonaws.com:9090/twitter'})
        twitter_query = QueryDict(r.content)
        UserProfile.insert_twitter_token(twitter_query, request.user)
        return HttpResponse(twitter_query['oauth_token'])
    else:
        error(request, 'Unsupported social network')
        response.status_code = 400
    response.write(''.join([item.message for item in get_messages(request)]))
    return response

@require_http_methods(['GET'])
def twitter(request):
    '''View function that
    '''
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_token_secret = UserProfile.objects\
                                    .filter(resource_owner_key=request.GET['oauth_token'])\
                                    .get().resource_owner_secret
    oauth = OAuth1(client_key=client_key,
                   client_secret=client_secret,
                   resource_owner_key=request.GET['oauth_token'],
                   resource_owner_secret=oauth_token_secret,
                   verifier=request.GET['oauth_verifier'])
    r = requests.post(url=access_token_url, auth=oauth)
    query = QueryDict(r.content)
    UserProfile.insert_account(request.GET['oauth_token'],
                               query, 2)
    t = Thread(target=social_init,
               args=(int(request.user.id),
                     query['oauth_token'],
                     query['oauth_token_secret']))
    t.daemon = True
    t.start()
    return HttpResponse(request.body)

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

@require_http_methods(['GET', 'POST'])
@login_required
def friends(request):
    if request.method == 'POST':
        Friend.update_favorite(request.user, loads(request.body))
    return JsonResponse(Friend.get_friends(request.user),
                        safe=False,
                        json_dumps_params={'indent': 2,
                                           'ensure_ascii': False})

@require_http_methods(['GET'])
@login_required
def favorite(request, offset):
    msg_list = Message.get_favorite_posts(request.user, int(offset))
    for i in range(len(msg_list)):
        msg_list[i]['time'] = msg_list[i]['time'].strftime('%a %b %d %H:%M:%S +0000 %Y')
    return JsonResponse(msg_list,
                        safe=False,
                        json_dumps_params={'indent': 2,
                                           'ensure_ascii': False})

@require_http_methods(['GET'])
@login_required
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
