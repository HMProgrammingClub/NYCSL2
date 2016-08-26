#!/bin/bash

apt-get install -y python3 python3-pip

apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.2.list
apt-get update -y
apt-get --assume-yes -y install mongodb-org

pip3 install -r requirements.txt
