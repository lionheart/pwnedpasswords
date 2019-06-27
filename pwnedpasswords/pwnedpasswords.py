#!/usr/bin/env python3

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

# Python 2 compatibility
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future import standard_library
from builtins import *

# urllib imports in Python 2.7
standard_library.install_aliases()

# Allow raise-from behavior in Python 2.7
from future.utils import raise_from

import sys
import hashlib
import logging
import re
import urllib.error
import urllib.request
from . import exceptions

looks_like_sha1_re = re.compile(r"^[a-fA-F0-9]{40}")

logger = logging.getLogger(__name__)

def check(password, plain_text=False, anonymous=True):
    password = Password(password, plain_text=plain_text)
    return password.check(anonymous=anonymous)

def search(password, plain_text=False):
    password = Password(password, plain_text=plain_text)
    return password.search()

def range(password, plain_text=False):
    password = Password(password, plain_text=plain_text)
    return password.range()

class PwnedPasswordsAPI(object):
    @staticmethod
    def url(*components, **kwargs):
        value = "https://api.pwnedpasswords.com/" + "/".join(components)
        if len(kwargs) > 0:
            value += "?" + urllib.parse.urlencode(kwargs)

        logger.info(value)
        return value

    @staticmethod
    def request(path, value, **kwargs):
        url = PwnedPasswordsAPI.url(path, value, **kwargs)
        request = urllib.request.Request(
            url=url,
            headers={
                'User-Agent': "pwnedpasswords (Python)"
            }
        )
        try:
            with urllib.request.urlopen(request) as f:
                response = f.read()
        except urllib.error.HTTPError as e:
            logger.debug("Exception found: {}".format(e))
            Exception = exceptions.STATUS_CODES_TO_EXCEPTIONS.get(e.code)
            if Exception is not None:
                exception = Exception(e.url, e.code, e.msg, e.hdrs, e.fp)
                raise_from(exception, e)
            else:
                raise
        else:
            return response.decode("utf-8-sig")

def convert_password_tuple(value):
    hash, count = value.split(":")
    return (hash, int(count))

class Password(object):
    def __init__(self, value, plain_text=False, verbosity=logging.WARNING):
        logger.setLevel(verbosity)

        if looks_like_sha1_re.match(value) and not plain_text:
            self.value = value
        else:
            # The provided value is plaintext, so let's hash it. If you'd like
            # to search the provided value as-is, specify `raw=True` in the
            # initializer.
            self.value = hashlib.sha1(value.encode("utf8")).hexdigest()

    def check(self, anonymous=True):
        if anonymous:
            entries = self.range()
            entry = entries.get(self.value[5:].upper())
            if entry is None:
                logger.info("No entry found, returning 0")
                return 0
            else:
                logger.info("Entry found")
                return entry
        else:
            return self.search()

    def search(self):
        try:
            kwargs = {}
#           if self.plaintext:
#               kwargs['originalPasswordIsAHash'] = "true"

            response = PwnedPasswordsAPI.request("pwnedpassword", self.value, **kwargs)
        except exceptions.PasswordNotFound:
            logger.info("No password found")
            return 0
        else:
            logger.info("Password found")
            count = int(response)
            return count

    def range(self):
        response = PwnedPasswordsAPI.request("range", self.value[:5].upper())
        entries = dict(map(convert_password_tuple, response.upper().split("\r\n")))
        return entries

