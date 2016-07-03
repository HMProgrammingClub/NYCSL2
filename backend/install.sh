#!/bin/bash
apt-get update -y
apt-get install -y -qq mongodb
pip3 install -r requirements.txt || pip install -r requirements.txt
