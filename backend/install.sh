#!/bin/bash
apt-get update -y
yes | apt-get install -y mongodb
pip3 install -r requirements.txt | pip install -r requirements.txt
