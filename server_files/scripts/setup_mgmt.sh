sudo apt update
sudo apt -y install python3-pip
sudo -u root pip3 install flask
sudo mkdir /usr/local/md5_mgmt/
sudo /usr/bin/wget https://www.asleague.org/res/temp/cs655/mgmt.tar.gz -O /usr/local/md5_mgmt/mgmt.tar.gz
sudo tar -zxvf /usr/local/md5_mgmt/mgmt.tar.gz -C /usr/local/md5_mgmt/
sudo rm /usr/local/md5_mgmt/mgmt.tar.gz
sudo systemctl enable systemd-networkd.service systemd-networkd-wait-online.service
sudo wget https://www.asleague.org/res/temp/cs655/systemd/mgmt.service -O /etc/systemd/system/startup.service
sudo systemctl daemon-reload
sudo systemctl enable startup
sudo systemctl start startup
