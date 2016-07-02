#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y python3-pip

yes | sudo apt-get install -y mongodb
sudo pip3 install -r requirements.txt
