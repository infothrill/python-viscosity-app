#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

v = open(os.path.join(os.path.dirname(__file__), 'viscosity_app', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='viscosity-app',
    version='0.1.0',
    description='Python Boilerplate contains all the boilerplate you need to create a Python package.',
    long_description=(open('README.rst', 'r').read() + '\n\n' +
                      open('HISTORY.rst', 'r').read()),
    author='Paul Kremer',
    author_email='paul@spurious.biz',
    url='https://github.com/infothrill/python-viscosity-app',
    packages=[
        'viscosity-app',
    ],
    package_dir={'viscosity-app': 'viscosity_app'},
    include_package_data=True,
    install_requires=[
        "py-applescript",
    ],
    license="MIT",
    zip_safe=True,
    keywords='viscosity-app',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
