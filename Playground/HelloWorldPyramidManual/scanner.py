from paste.httpserver import serve

if __name__ == '__main__':
    from pyramid.config import Configurator
    from hello import hello
    config = Configurator()
    config.scan('hello')
    config.add_route('default', '/', view=hello.hello)
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0')