class CorsMiddleware(object):
    def process_response(self, request, response):
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Origin'] = 'http://0.0.0.0:8100'
        return response
