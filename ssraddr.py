#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-
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

from depsb64 import *
from urllib.parse import parse_qs,urlsplit

allnodes = []

sample_nodeconf = \
    {
        "local_port": 1084,
        "fast_open": True,
        "password": None,
        "protocol_param": None,
        "protocol": None,
        "timeout": 120,
        "server_port": None,
        "connect_verbose_info": 1,
        "obfs": None,
        "udp_timeout": 60,
        "server_ipv6": "::",
        "dns_ipv6": False,
        "local_address": "0.0.0.0",
        "method": None,
        "obfs_param": None,
        "server": None,
        "remarks": None
    }

#['remarks'] = decode_base64(uri_node_query['remarks'][0].encode()).decode()

def ssr2conf_b64(ssrurilist):
    newssrurilst = []
    for i in ssrurilist:
        i = i.replace('ssr://','')
        i = i.encode()
        i = decode_base64(i)
        newssrurilst.append(i)
        # return elements in bytes
    # remarks saved here
    node_remarks = []
    for i in newssrurilst:
        i = i.decode()
        spl_symbol = i.find('/?')
        if spl_symbol == '-1':
            raise NotImplementedError
        serverparams = i[:spl_symbol]
        serverparams = serverparams.split(sep=':')
        urileft = i[spl_symbol:]
        uriparams_b64 = 'http://127.0.0.1' + urileft
        uri_node = urlsplit(uriparams_b64)
        uri_node_query = parse_qs(uri_node.query)
        try:
            node_remarks.append(decode_base64(uri_node_query['remarks'][0].encode()).decode())
        except:
            pass
    # choose the first node to develop useless params
    spe1node = newssrurilst[0]
    spe1node = spe1node.decode()
    spl_symbol = spe1node.find('/?')
    if spl_symbol == '-1':
        raise NotImplementedError
    serverparams = spe1node[:spl_symbol]
    serverparams = serverparams.split(sep=':')
    urileft = spe1node[spl_symbol:]
    uriparams_b64 = 'http://127.0.0.1' + urileft
    uri_node = urlsplit(uriparams_b64)
    sample_nodeconf['server_port'] = serverparams[1]
    sample_nodeconf['method'] = serverparams[3]
    sample_nodeconf['password'] = decode_base64(serverparams[5].encode()).decode()
    sample_nodeconf['protocol'] = serverparams[2]
    sample_nodeconf['obfs'] = serverparams[4]
    uri_node_query = parse_qs(uri_node.query)
    try:
        sample_nodeconf['obfs_param'] = decode_base64(uri_node_query['obfsparam'][0].encode()).decode()
    except KeyError:
        sample_nodeconf['obfs_param'] = ''
    try:
        sample_nodeconf['protocol_param'] = decode_base64(uri_node_query['protoparam'][0].encode()).decode()
    except KeyError:
        sample_nodeconf['protocol_param'] = ''
    # all servers listed
    for node in newssrurilst:
        node = node.decode()
        spl_symbol = node.find('/?')
        serverparams = node[:spl_symbol]
        serverparams = serverparams.split(sep=':')
        singleserver = serverparams[0]
        allnodes.append(singleserver)
    resultall = [sample_nodeconf,allnodes,node_remarks]
    return resultall

def singleuser():
    asku_passwd = input("Password?")
    asku_enc = input("Encryption method?")
    asku_serv = input("Server host?")
    asku_servport = int(input("Server port?"))
    asku_proto = input("Protocol?")
    asku_protopara = input("Protocol Params?")
    asku_obfs = input("OBFS?")
    asku_obfsparam = input("OBFS Params?")
    sample_nodeconf['password'] = asku_passwd
    sample_nodeconf['method'] = asku_enc
    sample_nodeconf['server'] = asku_serv
    sample_nodeconf['server_port'] =asku_servport
    sample_nodeconf['protocol'] = asku_proto
    sample_nodeconf['protocol_param'] = asku_protopara
    sample_nodeconf['obfs'] =asku_obfs
    sample_nodeconf['obfs_param'] = asku_obfsparam
    return sample_nodeconf