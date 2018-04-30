#!/usr/bin/env bash
usernow=$(whoami)
cd $(dirname $(readlink -f $0))
sudo python3 ./main.py
sudo cp ./clientconf.json ./shadowsocksr/shadowsocks/
python3 ./shadowsocksr/shadowsocks/local.py -c ./shadowsocksr/shadowsocks/clientconf.json
echo "Client successfully ran in the background!"
exit 0
