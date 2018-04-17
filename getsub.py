#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-
#
# Server Subscribe Extension for SSRR Client in Python
# Get subscribe details from SSPanel
# Copyright (C) 2018 Patrick Young
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from depsb64 import *
import json

import requests
import os


def loadsubcri():
    subscrconf = open(os.path.expanduser('./usersub.json'), 'r')
    subscrconf = subscrconf.read()
    subscrconf = json.loads(subscrconf)
    suburl = subscrconf['suburl']
    try:
        r = requests.get(suburl)
        b64_subaddrs = r.content
    except:
        b64_subaddrs = 'ERROR'
    return b64_subaddrs


def sub2ssraddrs(b64_subaddrs):
    byte_ssraddrs = decode_base64(b64_subaddrs)
    ssraddrslist = str(byte_ssraddrs.decode()).split(sep='\n')
    return ssraddrslist[:-1]


if __name__ == '__main__':
    print("Module as a part of SSRR Python Client Server Subscribe extension.")
