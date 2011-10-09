import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['pyramid', 'WebError']
# Add WebTest for TestApp functional testing per http://docs.pylonsproject.org/projects/pyramid/1.0/narr/testing.html
tests_require = requires[:].extend(['WebTest'])

setup(name='MCShoppingList',
      version='0.0',
      description='MCShoppingList',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      test_suite="mcshoppinglist",
      entry_points = """\
      [paste.app_factory]
      main = mcshoppinglist:main
      """,
      paster_plugins=['pyramid'],
      )

