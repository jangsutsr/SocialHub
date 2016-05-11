from django.http import HttpResponse

class CorsMiddleware(object):
    def process_request(self, request):
        if request.method == 'OPTIONS':
            response = HttpResponse(content_type='text/plain')
            response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
            response['Access-Control-Allow-Origin'] = 'http://0.0.0.0:8100'
            response['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type'
            return response

    def process_response(self, request, response):
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Origin'] = 'http://0.0.0.0:8100'
        if response['Content-Type'] == 'text/html; charset=utf-8':
            response['Content-Type'] = 'text/plain; charset=utf-8'
        return response
