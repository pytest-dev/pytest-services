"""Setuptools entry point."""
import codecs
import os
import sys
import re

from setuptools import setup

dirname = os.path.dirname(__file__)

long_description = (
    codecs.open(os.path.join(dirname, 'README.rst'), encoding='utf-8').read() + '\n' +
    codecs.open(os.path.join(dirname, 'AUTHORS.rst'), encoding='utf-8').read() + '\n' +
    codecs.open(os.path.join(dirname, 'CHANGES.rst'), encoding='utf-8').read()
)

install_requires = [
    'requests',
    'psutil',
    'pytest',
    'zc.lockfile >= 2.0',
]

PY2 = sys.version_info[0] < 3

if PY2:
    install_requires.append('subprocess32')

with codecs.open(os.path.join(dirname, "pytest_services", "__init__.py"), encoding="utf-8") as fd:
    VERSION = re.compile(r".*__version__ = ['\"](.*?)['\"]", re.S).match(fd.read()).group(1)


setup(
    name='pytest-services',
    description='Services plugin for pytest testing framework',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author='Anatoly Bubenkov, Paylogic International and others',
    license='MIT license',
    author_email='bubenkoff@gmail.com',
    version=VERSION,
    url='https://github.com/pytest-dev/pytest-services',
    install_requires=install_requires,
    extras={
        'memcached': ['pylibmc'],
    },
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ] + [('Programming Language :: Python :: %s' % x) for x in '2.7 3.4 3.5 3.6 3.7'.split()],
    tests_require=['tox'],
    entry_points={'pytest11': [
        'pytest-services=pytest_services.plugin',
    ]},
    packages=['pytest_services'],
)
