#!/usr/bin/env bash
cd $(dirname $(readlink -f $0))
python3 ./main.py
cp ./clientconf.json ./shadowsocksr/shadowsocks/
nohup python3 ./shadowsocksr/shadowsocks/local.py -c ./shadowsocksr/shadowsocks/clientconf.json > /dev/null 2>&1 &
echo "Client successfully ran in the background!"
exit 0
