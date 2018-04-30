#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-
#
# Server Subscribe Extension for SSRR Client in Python
# Main Process
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

from getsub import *
import os
import json
from ssraddr import *
from bestchoice import *

def main():
    # detect whether root or not.
    # we need root to use socket and send ICMP to test server
    runningby = os.getuid()
    if runningby == 0:
        pass
    else:
        print("To use speed check feature, this program must be run as root.")
        raise PermissionError
    # default workflow process
    try:
        subconf = open(os.path.expanduser('./usersub.json'), 'r')
        subconf.close()
    except FileNotFoundError:
        cwdirec = os.getcwd()
        os.chdir(cwdirec)
        os.system(os.path.expanduser('./1sttime.sh'))
        subconf = open(os.path.expanduser('./usersub.json'), 'r')
        subconf.close()
    except:
        print("Unknown Error! main.py@before_run test")
    subaddrs = loadsubcri()
    ssrurilst = sub2ssraddrs(subaddrs)
    ssrconfs = ssr2conf_b64(ssrurilst)
    cli_conf_samp = ssrconfs[0]
    bestserver = pcchoose(ssrconfs[1])
    if isinstance(bestserver,int):
        return print("Unknown Error! main.py@bestserver test")
    else:
        pass
    cli_conf_samp['server'] = bestserver
    dumpedconf = json.dumps(cli_conf_samp)
    dumpfile = open(os.path.expanduser('./clientconf.json'),'w')
    dumpfile.write(dumpedconf)
    dumpfile.close()
    print("Server subscribe extension successfully executed!")
    return 0

if __name__ == '__main__':
    askuser = int(input("Single user, Press 1; Server Sub, Press 2"))
    if askuser == 2:
        main()
    elif askuser == 1:
        cli_conf_samp = singleuser()
        dumpedconf = json.dumps(cli_conf_samp)
        dumpfile = open(os.path.expanduser('./clientconf.json'), 'w')
        dumpfile.write(dumpedconf)
        dumpfile.close()
    else:
        print("Illegal input!")
        os._exit(20)