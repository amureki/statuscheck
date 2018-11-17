#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = "\n" + f.read()

about = {}

with open(os.path.join(here, 'statuscheck', '__about__.py')) as f:
    exec(f.read(), about)

requirements = ['Click>=6.0', 'requests', 'requests_html', 'feedparser']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author=about['__author__'],
    author_email=about['__email__'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Tool to check PAAS/SAAS status pages",
    entry_points={
        'console_scripts': [
            'statuscheck=statuscheck.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=long_description,
    include_package_data=True,
    keywords='statuscheck',
    name='statuscheck',
    packages=find_packages(exclude=['tests', 'tests.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url=about['__url__'],
    version=about['__version__'],
    zip_safe=False,
)
