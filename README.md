# SSRR with Server Subscribe with Python3 on Linux

## Usage

**ATTENTION: THIS PROGRAM USE SOCKET TO TEST SERVER SPEED(BASED ON PING), SO YOU NEED TO RUN IT USING ROOT PERMISSION!**

1. **Only first time** Run ```sudo ./1sttime.sh``` to initialize config and install dependencies.
2. Fill in your subscribe URL in ```usersub.json``` "suburl". This URL should be provided by your SP.
3. Run ```sudo ./runclient.sh``` to get config and run SSRR Python client. Please follow the instructions shown on the screen.

## Support Details

The issues submitted to this repo must contains traceback log or error log, unless you want it to be directly closed.

### Useless info

#### Original Version

https://github.com/shadowsocksrr/shadowsocksr/tree/akkariiin/master

Original Version licensed under Apache License 2.0 (More details can be seen [here](http://www.apache.org/licenses/LICENSE-2.0.txt))

#### This Version

All code written by @kmahyyg are licensed under AGPL-3.0 (More details can be seen [here](https://www.gnu.org/licenses/agpl-3.0.txt))

And now, I made it great again. Speedtest feature using asyncio ping, Performance is boosted twice.

```bash
[root@host master /work] # time sudo ./runclient.sh
sudo ./runclient.sh  0.30s user 0.06s system 0% cpu 40.590 total
[root@host async_ping3 /work] # time sudo ./runclient.sh
sudo ./runclient.sh  0.40s user 0.06s system 2% cpu 17.864 total
```



# Polipo Config

Polipo can help you convert your socks5 proxy to a HTTP proxy easily.

```/etc/polipo/config```

```
socksParentProxy = "127.0.0.1:1084"
socksProxyType = socks5
proxyAddress = "::0"
proxyPort = 1085
logSyslog = true
logFile = /var/log/polipo/polipo.log
```

#### Opensource dependencies acknowledgement

1. Ping3 Originally from [here](https://github.com/kyan001/ping3/blob/master/LICENSE.txt), Licensed under MIT.
