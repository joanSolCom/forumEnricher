#!/bin/sh
/etc/init.d/apache2 start
chmod -R 777 /var/www/html/
IP=`tail -n 1 /etc/hosts | cut -f1`
python apanyer.py IP
python -u server.py
