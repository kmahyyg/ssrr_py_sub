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
from time import sleep
import asyncio

speedlist = []


def serverloca(servername):
    try:
        serverip = dnslookup(servername)
    except:
        print("DNS Error!")
        raise ConnectionError
    baseuri = 'http://freeapi.ipip.net/' + serverip
    sleep(1)
    r = requests.get(baseuri)
    sleep(1)
    if r.status_code > 310:
        print(r.status_code)
        serverlocation = 'Unknown'
        return serverlocation
    serverlocation = r.text
    return serverlocation


def pcchoose(serverlst):
    loop = asyncio.get_event_loop()
    tasklist = []
    for i in serverlst:
        tsk = asyncio.ensure_future(ping(i))
        tasklist.append(tsk)
    loop.run_until_complete(asyncio.gather(*tasklist))
    for i in tasklist:
        rtt = i.result()
        if isinstance(rtt, float):
            rtt = rtt * 1000
        elif rtt == None:
            rtt = 999999
        speedlist.append(rtt)
    fast_server_rtt = min(speedlist)
    fast_server = speedlist.index(fast_server_rtt)
    # list.index() only return one item
    # must tell user the fastest server hostname
    fast_server_host = serverlst[fast_server]
    locations = serverloca(fast_server_host)
    print("The Fastest Server is "+ fast_server_host + " @ " + locations)
    choice = input("Correct? (Y/N)")
    if choice.lower() == 'n':
        print('\n')
        print("--------Server List--------")
        for i in serverlst:
            print(i)
            cursvrno = serverlst.index(i)
            print('Latency: ' + str(speedlist[cursvrno]))
            print('\n',end='')
        print("--------Server Listed --------")
        print('\n')
        fast_server_host = input("Please Copy&Paste the server you want? ")
        return fast_server_host
    elif choice.lower() == 'n':
        return fast_server_host
    else:
        print("Illegal input!")
        return 2