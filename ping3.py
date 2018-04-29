#!/usr/bin/env python3
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

import asyncio
import functools
import socket
import struct
import sys
import threading
import time

import async_timeout  # installed from pip

__version__ = '1.1.1'

if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock()
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time()


# From /usr/include/linux/icmp.h; your milage may vary.
# ICMP types, defined in rfc792(ipv4) & rfc4443(ipv6)

ICMP_ECHO_REQUEST = 8  # Seems to be the same on Solaris.
ICMP6_ECHO_REQUEST = 128
ICMP_ECHO_REPLY = 0
ICMP6_ECHO_REPLY = 129

proto_icmp = socket.getprotobyname('icmp')  # 1
proto_icmp6 = socket.getprotobyname('ipv6-icmp')  # 58


def checksum(source_string):
    """
    I'm not too confident that this is right but testing seems
    to suggest that it gives the same answers as in_cksum in ping.c
    """
    sum = 0
    countTo = len(source_string)
    count = 0
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum = sum + thisVal
        count = count + 2

    if countTo < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff

    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


async def receive_one_ping(my_socket, ID, timeout):
    """
    receive the ping from the socket.
    """
    loop = asyncio.get_event_loop()
    timeLeft = timeout
    try:
        with async_timeout.timeout(timeout):
            while True:
                startedQueue = default_timer
                howLongInQueue = (default_timer - startedQueue)

                timeReceived = default_timer
                recPacket, addr = await loop.sock_recv(my_socket, 1024)
                if my_socket.family == socket.AF_INET:
                    offset = 20
                else:
                    offset = 0

                icmpHeader = recPacket[offset:offset + 8]

                type, code, checksum, packetID, sequence = struct.unpack(
                    "bbHHh", icmpHeader
                )
                # Filters out the echo request itself.
                # This can be tested by pinging 127.0.0.1
                # You'll see your own request
                if type != ICMP_ECHO_REPLY and type != ICMP6_ECHO_REPLY and packetID == ID:
                    bytesInDouble = struct.calcsize("d")
                    timeSent = struct.unpack("d", recPacket[offset + 8:offset + 8 + bytesInDouble])[0]
                    return timeReceived - timeSent

                timeLeft = timeLeft - howLongInQueue
                if timeLeft <= 0:
                    return None
    except asyncio.TimeoutError:
        return None


def sendto_ready(packet, socket, future, dest):
    socket.sendto(packet, dest)
    loop = asyncio.get_event_loop()
    loop.remove_writer(socket)
    future.set_result(None)


async def send_one_ping(my_socket, dest_addr, ID, family, timeout=4):
    """
    Send one ping to the given >dest_addr<.
    """
    dest_addr = socket.gethostbyname(dest_addr)

    global icmp_type
    if family == socket.AF_INET6:
        icmp_type = ICMP6_ECHO_REQUEST
    else:
        icmp_type = ICMP_ECHO_REQUEST

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    my_checksum = 0

    # Make a dummy header with a 0 checksum.
    header = struct.pack("bbHHh", icmp_type, 0, my_checksum, ID, 1)
    # ID: Low-endian identifier, bbHHh: network byte order
    bytesInDouble = struct.calcsize("d")
    data = (192 - bytesInDouble) * "Q"
    data = struct.pack("d", default_timer) + data.encode()

    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack("bbHHh", icmp_type, 0, socket.htons(my_checksum), ID, 1)
    packet = header + data

    loop = asyncio.get_event_loop()
    future = loop.create_future()
    callback = functools.partial(sendto_ready(packet=packet, socket=my_socket, dest=dest_addr, future=future))
    loop.add_writer(my_socket, callback)
    await future


async def ping(dest_addr, timeout=4):
    """
    Send one ping to destination address with the given timeout.

    Args:
        dest_addr: Str. The destination address. Ex. "192.168.1.1"/"example.com"
        timeout: Int. Timeout in seconds. Default is 4s, same as Windows CMD.

    Returns:
        The delay (in microseconds) or None on timeout.
    """

    loop = asyncio.get_event_loop()
    info = await loop.getaddrinfo(dest_addr, 0)
    family = info[2][0]
    addr = info[2][4]

    if family == socket.AF_INET:
        icmp = proto_icmp
    else:
        icmp = proto_icmp6

    try:
        global my_socket
        my_socket = socket.socket(family, socket.SOCK_RAW, icmp)
        my_socket.setblocking(False)
    except OSError as e:
        msg = e.strerror
        if e.errno == 1:
            msg += (
                " - Note that ICMP messages can only be sent from processes"
                " running as root."
            )

            raise OSError(msg)

    my_ID = threading.current_thread().ident & 0xFFFF
    await send_one_ping(my_socket, dest_addr, family, timeout=4)
    delay = await receive_one_ping(my_socket, my_ID, timeout)
    my_socket.close()

    if delay == None:
        return delay
    else:
        delay = int(delay * 1000)
        return delay


async def verbose_ping(dest_addr, timeout=4, count=4):
    """
    Send pings to destination address with the given timeout and display the result.

    Args:
        dest_addr: Str. The destination address. Ex. "192.168.1.1"/"example.com"
        timeout: Int. Timeout in microseconds. Default is 4s, same as Windows CMD.
        count: Int. How many pings should be sent. Default is 4, same as Windows CMD.

    Returns:
        Formatted ping results printed.
    """
    for i in range(count):
        print("ping '{}' ... ".format(dest_addr), end='')
        try:
            delay = await ping(dest_addr, timeout)
        except socket.gaierror as e:
            print("Failed. (socket error)")
            break
        except Exception as e2:
            print("{destaddr} failed: {msg}".format(destaddr=dest_addr, msg=str(e2)))

        if delay is None:
            print("Timeout > {}s".format(timeout))
        else:
            print("{}ms".format(int(delay)))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    tasks = [
        asyncio.ensure_future(verbose_ping('qq.com')),
        asyncio.ensure_future(verbose_ping('192.168.1.1')),
        asyncio.ensure_future(verbose_ping('baidu.com'))
    ]

    loop.run_until_complete(asyncio.gather(*tasks))
