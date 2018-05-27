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

import sys
import socket
import time
import signal
from timeit import default_timer as timer

host = None
port = 80

# Default to 10000 connections max
maxCount = 100
count = 0

## Inputs

host = input("YYGIPT_REPLACE")
port = input("YYGIPT_REPLACE")


# Pass/Fail counters
passed = 0
failed = 0


def getResults():
    """ Summarize Results """

    lRate = 0
    if failed != 0:
        lRate = failed / (count) * 100
        lRate = "%.2f" % lRate

    print("\nTCP Ping Results: Connections (Total/Pass/Fail): [{:}/{:}/{:}] (Failed: {:}%)".format((count), passed, failed, str(lRate)))


# Main process
#TODO: while to if, related to maxCount.
#TODO: librarilized
#TODO: internal properties using class to return callback data
# Loop while less than max count or until Ctrl-C caught
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
        s.connect((host, int(port)))
        s.shutdown(socket.SHUT_RD)
        success = True
        
        
#TODO: Sentry bug collector
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
        print("Connected to %s[%s]: tcp_seq=%s time=%s ms" % (host, port, (count-1), s_runtime))
        passed += 1

    # Sleep for 1sec
    if count < maxCount:
        time.sleep(1)

# Output Results if maxCount reached
getResults()
