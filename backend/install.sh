#!/bin/bash
apt-get update -y
apt-get --assume-yes -y install mongodb
pip3 install -r requirements.txt || pip install -r requirements.txt
