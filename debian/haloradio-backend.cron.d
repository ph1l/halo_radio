#
# Regular cron jobs for the haloradio-backend package
#
*/15 * * * * radio nice /usr/share/haloradio/cron.often.sh
12 5 * * * radio nice /usr/share/haloradio/cron.daily.sh

