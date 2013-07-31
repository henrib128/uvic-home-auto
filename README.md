uvic-home-auto
==============

cd /opt
sudo mkdir pimation playbacks mjpg-streamer
sudo chown pi pimation playbacks mjpg-streamer
sudo chgrp pi pimation playbacks mjpg-streamer

svn co https://mjpg-streamer.svn.sourceforge.net/svnroot/mjpg-streamer/mjpg-streamer mjpg-streamer
cd mjpg-streamer
make
sudo make install
cd ..

git clone git@github.com:henrib128/uvic-home-auto.git pimation

cd pimation
./scripts/deploy_web.sh

sudo cp scripts/pimation /etc/init.d/
sudo chmod 755 /etc/init.d/pimation
sudo update-rc.d pimation defaults
