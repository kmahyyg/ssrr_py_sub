# SSRR Server Subscribe Extension for Python Client

# Original Version

https://github.com/shadowsocksrr/shadowsocksr/tree/akkariiin/master

Original Version licensed under Apache License 2.0 (More details can be seen [here](http://www.apache.org/licenses/LICENSE-2.0.txt))

# This Version

All code written by @kmahyyg are licensed under AGPL-3.0 (More details can be seen [here](https://www.gnu.org/licenses/agpl-3.0.txt))

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