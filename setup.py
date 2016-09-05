#!/usr/bin/env python

import os
from setuptools import setup, find_packages

from tests import test_cmd


ROOT = os.path.dirname(__file__)


def read(fname):
    return open(os.path.join(ROOT, fname)).read()


setup(
    name="django-fusion-tables",
    version="0.9",
    url="https://github.com/bsvetchine/django-fusion-tables",
    license="MIT",
    description="",
    long_description=read("README.rst"),
    author="Bertrand Svetchine",
    author_email="bertrand.svetchine@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read("requirements.txt").splitlines(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    cmdclass={'test': test_cmd.TestCommand}
)
