# TODO Introduce a proper dependency injection framework. (Spring Python?)

class DependencyResolver(object):
    _etag_manager = None
    _etag_manager_factory = None

    @staticmethod
    def register_etag_manager_factory(etag_manager_factory):
        DependencyResolver._etag_manager_factory = etag_manager_factory
        #DependencyResolver._etag_manager = etag_manager

    @staticmethod
    def get_etag_manager():
        if not DependencyResolver._etag_manager:
            DependencyResolver._etag_manager = DependencyResolver._etag_manager_factory.create()
        return DependencyResolver._etag_manager
    
