#!/usr/bin/env bash
cp ./subconf.json.eg ./usersub.json
sudo pip3 install -r ./requirements.txt
git submodule init
git submodule update
echo "Done!"
exit 0