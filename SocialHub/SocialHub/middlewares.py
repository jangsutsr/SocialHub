from django.shortcuts import redirect

class CheckUserMiddleware(object):
    def process_request(self, request):
        if ('user' not in request.session and
            request.path not in ('/login', '/register')):
            return redirect('/login')
