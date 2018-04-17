#!/usr/bin/env python3.6
#-*- encoding: utf-8 -*-
#
# Server Subscribe Extension for SSRR Client in Python
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

from ping3 import ping
from socket import gethostbyname as dnslookup
import requests


speedlist = []


def serverloca(servername):
    try:
        serverip = dnslookup(servername)
    except:
        print("DNS Error!")
        return 1
    baseuri = 'http://freeapi.ipip.net/' + serverip
    r = requests.get(baseuri)
    serverlocation = r.text
    return serverlocation


def pcchoose(serverlst):
    for node in serverlst:
        rtt = ping(node)
        speedlist.append(rtt)
    fast_server_rtt = min(speedlist)
    fast_server = speedlist.index(fast_server_rtt)
    # list.index() only return one item
    # must tell user the fastest server hostname
    fast_server_host = serverlst[fast_server]
    locations = serverloca(fast_server_host)
    print("The Fastest Server is "+ fast_server_host + "@" + locations)
    choice = input("Correct? (Y/N)")
    if choice == 'N':
        print('\n')
        print("--------Server List--------")
        for i in serverlst:
            print(i)
        print("--------Server Listed --------")
        print('\n')
        fast_server_host = input("Please Copy&Paste the server you want? ")
        return fast_server_host
    elif choice == 'Y':
        return fast_server_host
    else:
        print("Illegal input!")
        return 2