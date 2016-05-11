class CorsMiddleware(object):
    def process_response(self, request, response):
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Origin'] = 'http://0.0.0.0:8100'
        if response['Content-Type'] == 'text/html; charset=utf-8':
            response['Content-Type'] = 'text/plain; charset=utf-8'
        return response
