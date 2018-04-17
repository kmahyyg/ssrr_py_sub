#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-

from depsb64 import *
import os
import json
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
        "server": None
    }


def ssr2conf_b64(ssrurilist):
    for i in ssrurilist:
        i = i.replace('ssr://','')
        i = i.encode()
        i = decode_base64(i)
        # return elements in bytes
    # choose the first node to develop useless params
    spe1node = ssrurilist[0]
    spe1node = spe1node.decode()
    spl_symbol = spe1node.find('/?')
    serverparams = spe1node[:spl_symbol]
    serverparams = serverparams.split(sep=':')
    urileft = spe1node[spl_symbol:]
    uriparams_b64 = 'http://127.0.0.1' + urileft
    uri_node = urlsplit(uriparams_b64)
    sample_nodeconf['server_port'] = serverparams[1]
    sample_nodeconf['method'] = serverparams[3]
    sample_nodeconf['password'] = decode_base64(spe1node[5])
    sample_nodeconf['protocol'] = serverparams[2]
    sample_nodeconf['obfs'] = serverparams[4]
    uri_node_query = parse_qs(uri_node.query)
    sample_nodeconf['obfs_param'] = decode_base64(uri_node_query['obfsparam'][0])
    sample_nodeconf['protocol_param'] = decode_base64(uri_node_query['protoparam'][0])
    # all servers listed
    for node in ssrurilist:
        node = node.decode()
        spl_symbol = node.find('/?')
        serverparams = node[:spl_symbol]
        serverparams = serverparams.split(sep=':')
        singleserver = serverparams[0]
        allnodes.append(singleserver)
    resultall = [sample_nodeconf,allnodes]
    return resultall