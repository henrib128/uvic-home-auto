#!/bin/bash
# Clean /var/www/
sudo rm /var/www/*

# Copy over revelvant website files
sudo cp style.css /var/www/
sudo cp *.php /var/www/
sudo cp *.jpg /var/www/
sudo cp *.png /var/www/

