# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import atp
version = atp.__version__

setup(
    name='atoutpass',
    version=version,
    author='',
    author_email='youpsla@gmail.com',
    packages=[
        'atp',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.5',
    ],
    zip_safe=False,
    scripts=['atp/manage.py'],
)