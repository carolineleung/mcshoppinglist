import os
import sys

def main():
    # TODO Use path relative to... what?
    #sys.path.append('M:/src/_personal/pywebplayground/Playground/helloWorldService')
    cur_path_str = '{0}'.format(os.path.curdir)
    sys.path.append(os.path.abspath(cur_path_str + '/../../'))
    sys.path.append(os.path.abspath(cur_path_str))
    #sys.path.append('C:/mel/hg-repo/atom-hg3/Playground/DjangoRestServer/helloWorldService')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    import settings
    from django.core import management

    print('Python %s on %s' % (sys.version, sys.platform))
    print('Sys path: %s' % sys.path)
    management.setup_environ(settings)

if __name__ == "__main__":
    main()