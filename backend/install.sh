#!/bin/bash
sudo apt-get update -y

sudo apt-get install -y mongodb-server
sudo mkdir -p /data/db/
sudo chown `id -u` /data/db

sudo apt-get install -y python3-pip
sudo pip3 install -r requirements.txt || sudo pip install -r requirements.txt
