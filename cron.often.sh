#!/bin/sh
#
#

cd ~radio

(echo;date;echo) >> /var/log/haloradio/cron.often.log

./DBSync.py -fp >> /var/log/haloradio/cron.often.log

