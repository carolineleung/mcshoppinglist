def main(global_config, **settings):
    from mcshoppinglist.wsgiapp.wsgimain import wsgimain
    return wsgimain(global_config, **settings)

