#!/usr/bin/env/python
# -*- coding: utf-8 -*-

# Copyright 2018 Lionheart Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from distutils.cmd import Command
import os
import re
import unittest
import runpy

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

metadata_filename = "pwnedpasswords/metadata.py"
metadata = runpy.run_path(metadata_filename)

with open(os.path.join(os.path.dirname(__file__), "README.md")) as file:
    long_description = file.read()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
]

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from test_pwnedpasswords import TestPwnedPasswords
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPwnedPasswords)
        unittest.TextTestRunner(verbosity=2).run(suite)


setup(
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    classifiers=classifiers,
    description="A Python wrapper for Troy Hunt's Pwned Passwords API.",
    install_requires=["future"],
    keywords="passwords security",
    license=metadata['__license__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='pwnedpasswords',
    package_data={'': ['LICENSE', 'README.rst']},
    packages=['pwnedpasswords'],
    url="https://github.com/lionheart/pwnedpasswords",
    download_url="https://github.com/lionheart/pwnedpasswords/tarball/{}".format(metadata['__version__']),
    version=metadata['__version__'],
    scripts=["bin/pwnedpasswords"],
    test_suite='nose.collector',
    tests_require=['nose', 'future'],
)
