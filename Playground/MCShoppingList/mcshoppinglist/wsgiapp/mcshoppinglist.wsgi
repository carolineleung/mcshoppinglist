import os
import sys

"""
You can test that this file works by invoking it with the SAME path that mod_wsgi will use.
Invoking it with a relative path may lead to an incorrect "project_top".
e.g.
python /srv/mcshoppinglist/development/Playground/MCShoppingList/mcshoppinglist/wsgiapp/mcshoppinglist.wsgi
"""

currentPath = os.path.dirname(__file__)
if currentPath not in sys.path:
    sys.path.append(currentPath)
try:
    project_top = os.path.abspath(currentPath + '../../..')
    if project_top not in sys.path:
        sys.path.append(project_top)
except:
    print sys.exc_info()
    raise Exception('Failed to determine parent directory.')

from pyramid.paster import get_app
#application = get_app(project_top + '/development.ini', 'main')
application = get_app(project_top + '/production.ini', 'main')

