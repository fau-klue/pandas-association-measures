#!/usr/bin/env python3

import os
import sys
from setuptools import find_packages, setup, Command, Extension

# Package meta-data.
NAME = 'association-measures'
DESCRIPTION = 'Statistical association measures for Python pandas'
URL = 'https://github.com/fau-klue/pandas-association-measures'
EMAIL = 'philipp.heinrich@fau.de'
AUTHOR = 'Philipp Heinrich & Markus Opolka'

REQUIRES_PYTHON = '>=3.9'
REQUIRED = [
    'wheel',
    'pandas>=2.2.2,<3.0',
    'numpy>=2.0,<3.0',
    'scipy>=1.13.0,<2.0',
    # 'rbo>=0.1.3,<0.2'
]

here = os.path.abspath(os.path.dirname(__file__))

# description
with open(os.path.join(here, 'README.md'), encoding="utf-8") as f:
    long_description = f.read()

# version
version = {}
with open(os.path.join(here, 'association_measures', 'version.py'), encoding="utf-8") as f:
    exec(f.read(), version)


# Import Cython if available
try:
    from Cython.Build import cythonize
    CYTHON_INSTALLED = True
    extensions = [Extension('association_measures.binomial', ['association_measures/binomial.pyx'])]
except ImportError:
    cythonize = lambda x, *args, **kwargs: x  # dummy func
    CYTHON_INSTALLED = False
    extensions = [Extension('association_measures.binomial', ['association_measures/binomial.c'])]


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
            os.rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(version['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
    version=version['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
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
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Cython',
    ],
)
