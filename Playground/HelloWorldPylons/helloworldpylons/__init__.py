from pyramid.config import Configurator
from helloworldpylons.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('helloworldpylons.views.my_view',
                    context='helloworldpylons:resources.Root',
                    renderer='helloworldpylons:templates/mytemplate.pt')
    config.add_static_view('static', 'helloworldpylons:static')
    return config.make_wsgi_app()

