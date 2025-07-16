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


setup(
    name='pytest-services',
    description='Services plugin for pytest testing framework',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author='Anatoly Bubenkov, Paylogic International and others',
    license='MIT',
    author_email='bubenkoff@gmail.com',
    url='https://github.com/pytest-dev/pytest-services',
    extras={
        'memcached': ['pylibmc'],
    },
    python_requires=">=3.9",
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
    tests_require=['tox'],
    entry_points={'pytest11': [
        'pytest-services=pytest_services.plugin',
    ]},
    packages=['pytest_services'],
)
