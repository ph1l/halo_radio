#
# Regular cron jobs for the haloradio package
#
*/5 * * * * radio nice /usr/share/haloradio/halostatcron.sh
*/15 * * * * radio nice /usr/share/haloradio/cron.often.sh
12 5 * * * radio nice /usr/share/haloradio/cron.daily.sh

