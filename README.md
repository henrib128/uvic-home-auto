uvic-home-auto
==============

cd /opt
sudo mkdir pimation playbacks mjpg-streamer
sudo chown pi pimation playbacks mjpg-streamer
sudo chgrp pi pimation playbacks mjpg-streamer

sudo apt-get install libjpeg8-dev
sudo apt-get install imagemagick
svn co https://mjpg-streamer.svn.sourceforge.net/svnroot/mjpg-streamer/mjpg-streamer mjpg-streamer
cd mjpg-streamer
make
sudo make install
cd ..

git clone git@github.com:henrib128/uvic-home-auto.git pimation

cd pimation
./deploy_web.sh

sudo cp scripts/pimation /etc/init.d/
sudo chmod 755 /etc/init.d/pimation
sudo update-rc.d pimation defaults

============================

sudo mkdir /etc/apache2/ssl
cd /etc/apache2/ssl
sudo a2ensite default-ssl
sudo a2enmod ssl
sudo service apache2 restart

sudo /usr/sbin/make-ssl-cert /usr/share/ssl-cert/ssleay.cnf /etc/apache2/ssl/apache.crt
# enter public ip for host name and leave others blank

sudo cp apache.crt apache.pem
sudo cp apache.crt apache.key
sudo chmod 600 apache.key

sudo nano /etc/apache2/sites-enabled/default-ssl
# change:
SSLCertificateFile /etc/ssl/certs/ssl-cert-snakeoil.pem
SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key
# to:
SSLCertificateFile /etc/apache2/ssl/apache.pem
SSLCertificateKeyFile /etc/apache2/ssl/apache.key

sudo service apache2 restart

============================


