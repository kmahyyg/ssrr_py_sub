#!/usr/bin/env python3
"""
Upstream: https://github.com/yantisj/tcpping
Modified by kmahyyg

Builtin lib: https://docs.python.org/3/library/timeit.html

Use the same license with the upstream.
Licensed under GNU AGPL v3.

    TCP PING for ssrr_python_cli_subext
    Copyright (C) 2018 yantisj&kmahyyg

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import socket
import time
from timeit import default_timer as timer

# Loop while less than max count
# Inputs: host and port vars

class tcplatency(object):
    def __init__(self, host, port=543, debug=False):
        self.host = host
        self.port = port
        self.__time = 9999.00
        self.debug = debug

    def tcpping(self):
        # Recore latency using a list
        ping_latency = []
        # Default to 3 TCP PING packets max
        maxCount = 3
        count = 0
        # Pass/Fail counters
        passed = 0
        failed = 0
        while count < maxCount:
            # Increment Counter
            count += 1
            success = False
            # New Socket
            s = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            # 1sec Timeout
            s.settimeout(1)
            # Start a timer
            s_start = timer()
            # Try to Connect
            try:
                s.connect((self.host, int(self.port)))
                s.shutdown(socket.SHUT_RD)
                success = True
            # Connection Timed Out
            except socket.timeout:
                print("Connection timed out!")
                failed += 1
            except OSError as e:
                print("OS Error:", e)
                failed += 1
            # Stop Timer
            s_stop = timer()
            s_runtime = "%.2f" % (1000 * (s_stop - s_start))
            if success:
                ping_latency.append(float(s_runtime))
                passed += 1
            else:
                ping_latency.append(float(999.00))
                failed +=1
            # Sleep for 1sec
            if count < maxCount:
                time.sleep(1)
        if self.debug == True:
            self.__alltime = ping_latency
        avg_timeout = 0.00
        for i in ping_latency:
            avg_timeout += i
        avg_timeout = avg_timeout / 3.00
        self.__time = avg_timeout

    def gettime(self):
        if self.__time == 9999.00:
            print("Latency is not tested before, auto-perform a test now.")
            self.tcpping()
        return self.__time

    def getdbginfo(self):
        try:
            return self.__alltime
        except AttributeError:
            print("Debuggable: False!")