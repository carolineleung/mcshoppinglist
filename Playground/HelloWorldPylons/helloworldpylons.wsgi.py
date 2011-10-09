import os, sys
#sys.path.append('M:/src/_personal/mcshoppinglist/Playground/HelloWorldPylons')
os.environ['PYTHON_EGG_CACHE'] = 'M:/tmp/tmp'

# Setup virtualenv
# http://pypi.python.org/pypi/virtualenv
activate_this = 'M:/src/_personal/mcshoppinglist/Playground/pyenv/Scripts/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


from paste.deploy import loadapp
# Load Pyramid/Pylons config
# http://docs.pylonsproject.org/projects/pyramid/1.0/tutorials/modwsgi/index.html#modwsgi-tutorial
application = loadapp('config:M:/src/_personal/mcshoppinglist/Playground/HelloWorldPylons/development.ini')
  