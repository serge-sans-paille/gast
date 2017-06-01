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
      version='0.1.5',
      packages=['gast'],
      description='Python AST that abstracts the underlying Python version',
      author='serge-sans-paille',
      author_email='serge.guelton@telecom-bretagne.eu',
      license="BSD 3-Clause",
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3'],
      **kw
      )
