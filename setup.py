""" JBoss Python Client for interacting with Management API
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jboss-py',
    version='0.0.1',
    description='JBoss Python Client',
    long_description=long_description,
    url='https://github.com/jairojunior/jboss-py',
    author='Jairo Junior',
    author_email='junior.jairo1@gmail.com',
    license='Apache-2.0',
    keywords='jboss client api',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests'],
    extras_require={
        'dev': ['pylint'],
        'test': ['py-test'],
    },
)
