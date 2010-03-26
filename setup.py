import os
from setuptools import setup, find_packages

setup(name='galaxyvalidator',
    version='.'.join(map(str, __import__('galaxyvalidator').__version__)),
    description='Source code for GalaxyValidator.com',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/dcramer/galaxyvalidator',
    packages=find_packages(),
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)
