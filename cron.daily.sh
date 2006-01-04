#!/bin/sh
#
#

cd ~radio

cat /dev/null > /var/log/haloradio/cron.often.log

(echo;date;echo) > /var/log/haloradio/cron.daily.log

./DBSync.py -cfsp >> /var/log/haloradio/cron.daily.log

