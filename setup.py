#!/usr/bin/env python3


import io
import os
import sys
from setuptools import find_packages, Command
from distutils.core import setup
from distutils.extension import Extension

# Package meta-data.
NAME = 'association-measures'
DESCRIPTION = 'Corpus association measures for Python pandas'
URL = 'https://github.com/fau-klue/pandas-association-measures'
EMAIL = 'markus@martialblog.de'
AUTHOR = 'Markus Opolka'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = None

REQUIRED = [
    'pandas'
]

here = os.path.abspath(os.path.dirname(__file__))


# Import Cython if available
try:
    from Cython.Build import cythonize
    CYTHON_INSTALLED = True
    extensions = [Extension('association_measures.binomial', ['association_measures/binomial.pyx'])]
except ImportError:
    cythonize = lambda x, *args, **kwargs: x # dummy func
    CYTHON_INSTALLED = False
    extensions = [Extension('association_measures.binomial', ['association_measures/binomial.c'])]


LONG_DESCRIPTION = """
Corpus association measures for Python pandas.

Association measures are mathematical formulae that interpret cooccurrence frequency data. For each pair of words extracted from a corpus, they compute an association score, a single real value g that indicates the amount of (statistical) association between the two words.
"""

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "test_*"]),
    ext_modules=cythonize(extensions),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Cython',
    ],
)
