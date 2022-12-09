sudo apt update
sudo apt -y install python3-pip
sudo -u root pip3 install flask
sudo mkdir /usr/local/md5_node/
sudo /usr/bin/wget https://www.asleague.org/res/temp/cs655/node.tar.gz -O /usr/local/md5_node/node.tar.gz
sudo tar -zxvf /usr/local/md5_node/node.tar.gz -C /usr/local/md5_node/
sudo rm /usr/local/md5_node/node.tar.gz
sudo systemctl enable systemd-networkd.service systemd-networkd-wait-online.service
sudo wget https://www.asleague.org/res/temp/cs655/systemd/node.service -O /etc/systemd/system/startup.service
sudo systemctl daemon-reload
sudo systemctl enable startup
sudo systemctl start startup
