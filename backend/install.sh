#!/bin/bash
sudo apt-get update -y

sudo apt-get install -y python3 python3-pip mongodb 
sudo pip3 install -r requirements.txt || sudo pip install -r requirements.txt
