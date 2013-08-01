uvic-home-auto
====================================================================================

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

====================================================================================

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

====================================================================================

sudo apt-get install libapache2-mod-auth-mysql

mysql -u root -p
USE pihome;

CREATE TABLE Users (
	username varchar(40) NOT NULL default '',
	pass varchar(60) NOT NULL default '',
	is_admin BOOLEAN,
	PRIMARY KEY (username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO Users VALUES('guest', SHA1('guest'), false);
INSERT INTO Users VALUES('admin', SHA1('pimation'), true);

exit

sudo nano /etc/apache2/apache2.conf
# add the following:
<Directory /var/www>
	## mod auth_mysql
	AuthBasicAuthoritative Off
	AuthMYSQL on
	AuthMySQL_Authoritative on
	AuthMySQL_DB pihome
	Auth_MySQL_Host localhost
	Auth_MySQL_User ceng499
	Auth_MySQL_Password ceng499
	AuthMySQL_Password_Table Users
	AuthMySQL_Username_Field username
	AuthMySQL_Password_Field pass
	AuthMySQL_Empty_Passwords off
	AuthMySQL_Encryption_Types SHA1Sum
	# Standard auth stuff
	AuthType Basic
	AuthName "Pimation"
	Require valid-user
	AuthUserFile /dev/null
</Directory>

cd /etc/apache2/mods-enabled/
sudo ln -s /etc/apache2/mods-available/auth_mysql.load .
sudo service apache2 restart

====================================================================================




