from pyramid.response import Response
from pyramid.view import view_config

@view_config(name='hello', request_method='GET')
def hello(request):
    return Response('Hello world.')