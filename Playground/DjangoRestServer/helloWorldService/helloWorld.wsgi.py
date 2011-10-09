import os
import sys

currentPath = os.path.dirname(__file__)
if currentPath not in sys.path:
    sys.path.append(currentPath)

# TODO This "works" but then we lose the CSS for the admin site among other things.
#sys.path.append(currentPath + '/helloWorldService')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

###############################

# http://code.google.com/p/modwsgi/wiki/DebuggingTechniques
#class CustomDebugger:
#
#    def __init__(self, object):
#        self.__object = object
#
#    def __call__(self, *args, **kwargs):
#        import pdb, sys
#        debugger = pdb.Pdb()
#        debugger.use_rawinput = 0
#        debugger.reset()
#        sys.settrace(debugger.trace_dispatch)
#
#        try:
#            return self.__object(*args, **kwargs)
#        finally:
#            debugger.quitting = 1
#            sys.settrace(None)

###############################

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# application = CustomDebugger(application)



# Original WSGI hello world:
## http://code.google.com/p/modwsgi/wiki/QuickConfigurationGuide
#def application(environ, start_response):
#    status = '200 OK'
#    output = 'This is helloWorld.wsgi.py'
#    output += os.path.dirname(__file__)
#
#    response_headers = [('Content-type', 'text/plain'),
#                        ('Content-Length', str(len(output)))]
#    start_response(status, response_headers)
#
#    return [output]
