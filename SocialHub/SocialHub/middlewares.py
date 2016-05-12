from django.http import HttpResponse
from json import loads

class CorsMiddleware(object):
    '''Middleware for handling cross-origin resource share.
    '''
    def process_request(self, request):
        '''Respond to OPTIONS method to grant access previliges.
        '''
        if request.method == 'OPTIONS':
            response = HttpResponse(content_type='text/plain')
            response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
            response['Access-Control-Allow-Origin'] = 'http://0.0.0.0:8100'
            response['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type'
            return response

    def process_response(self, request, response):
        '''Add necessary headers to response.
        '''
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Origin'] = 'http://0.0.0.0:8100'
        if response['Content-Type'] == 'text/html; charset=utf-8':
            response['Content-Type'] = 'text/plain; charset=utf-8'
        return response

class JsonToQueryMiddleware(object):
    '''Middleware for converting json to query string.

    This middleware is needed because Angular tacitly converts query string
    to json format, which disables form validation. So it coverts json back
    to form query string when needed.
    '''
    def process_request(self, request):
        '''Convert json to query string by populating request.POST when needed.
        '''
        if request.method == 'POST' and \
            request.META.get('HTTP_ACCEPT', None) == 'application/json':
            try:
                post = request.POST.copy()
                form = loads(request.body)
                if type(form) == dict:
                    for key, value in form.iteritems():
                        post[key] = value
                    request.POST = post
            except Exception:
                pass
