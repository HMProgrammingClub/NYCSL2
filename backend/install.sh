sudo apt-get install -y mongodb-server
sudo mkdir -p /data/db/
sudo chown `id -u` /data/db

sudo pip3 install -r requirements.txt
