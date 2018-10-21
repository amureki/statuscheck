#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ['Click>=6.0', 'requests', 'requests_html']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Rustem Saiargaliev",
    author_email='r.saiargaliev@gmail.com',
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
    long_description=readme,
    include_package_data=True,
    keywords='statuscheck',
    name='statuscheck',
    packages=find_packages(exclude=['tests', 'tests.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/amureki/statuscheck',
    version='0.1.0',
    zip_safe=False,
)
