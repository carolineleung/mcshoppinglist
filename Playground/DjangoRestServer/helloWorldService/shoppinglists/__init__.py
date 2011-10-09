from dependencyresolver import DependencyResolver
from etags.etagmanager import EtagManager

# TODO This is makeshift dependency injection
class EtagManagerFactory(object):
    def create(self):
        return EtagManager()

DependencyResolver.register_etag_manager_factory(EtagManagerFactory())