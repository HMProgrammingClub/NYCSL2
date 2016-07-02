#!/bin/bash
sudo apt-get update -y

yes | sudo apt-get install -y mongodb
sudo -H pip install -r requirements.txt
