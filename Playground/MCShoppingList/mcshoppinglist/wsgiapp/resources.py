class Root(object):
    """
    Pyramid (Pylons) Root resource.
    """
    def __init__(self, request):
        self.request = request
