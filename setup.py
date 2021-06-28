# Use the newer `setuptools.setup()`, if available.
try:
    from setuptools import setup
    kw = {
        'test_suite': 'tests',
        'tests_require': ['astunparse'],
    }
except ImportError:
    from distutils.core import setup
    kw = {}

setup(name='gast',  # gast, daou naer!
      version='0.4.0',
      packages=['gast'],
      description='Python AST that abstracts the underlying Python version',
      long_description='''
A generic AST to represent Python2 and Python3's Abstract Syntax Tree(AST).

GAST provides a compatibility layer between the AST of various Python versions,
as produced by ``ast.parse`` from the standard ``ast`` module.''',
      author='serge-sans-paille',
      author_email='serge.guelton@telecom-bretagne.eu',
      url='https://github.com/serge-sans-paille/gast/',
      license="BSD 3-Clause",
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Programming Language :: Python :: 3.10',
                   ],
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
      **kw
      )
