import io
import re

from setuptools import setup


def read(fname):
    with open(fname, 'r') as f:
        return f.read()


def version():
    with io.open("jcson/__init__.py", "rt", encoding="utf8") as f:
        return re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(name             = 'jcson',
      description      = 'jcson - enhanced json for configuration',
      long_description = read('README.md'),
      version          = version(),
      author           = 'Alex Revetchi',
      author_email     = 'alex.revetchi@gmail.com',
      url              = 'https://github.com/zakalibit/jcson',
      packages         =['jcson'],
      license          = 'License :: OSI Approved :: MIT License',
      platforms        = 'Linux',
      classifiers      = [
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python'
          ]
    )