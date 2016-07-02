#!/bin/bash
sudo apt-get update -y

yes | sudo apt-get install -y mongodb 
sudo pip install -r requirements.txt
