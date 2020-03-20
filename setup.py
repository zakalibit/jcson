from setuptools import setup

def read(fname):
    with open(fname, 'r') as f:
        return f.read()

setup(name             = 'jcson',
      description      = 'jcson - enhanced json for configuration',
      long_description = read('README.md'),
      py_modules       = ['jcson'],
      version          = '0.1.0',
      author           = 'Alex Revetchi',
      author_email     = 'alex.revetchi@gmail.com',
      url              = 'https://github.com/zakalibit/jcson',
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
          ],
      )