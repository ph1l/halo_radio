#!/bin/sh
#
#
# halo_radio daemontools setup script.
#
# you may want to edit the definitions below here:

log_user=radiolog
log_group=radiolog
daemon_user=radio
daemon_group=radio
supervize_dir=/etc/haloradio/svsdir
daemon_dir=/usr/share/haloradio

#
# you shouldn't need to touch anything below here.. maybe..
#

echo

if [ -e ${supervize_dir} ];then
	exit 0
fi

if [ ! -e ${daemon_dir}/radiod.sh ]; then
	echo "daemon_dir (${daemon_dir}) doesn't exist"
	exit 255
fi

umask 022

mkdir ${supervize_dir} || exit 255
chmod 03755 ${supervize_dir} || exit 255
cd ${supervize_dir} || exit 255
printf "#!/bin/sh\n\n# halo_radio init script for daemontools\n\nexec setuidgid %s %s/radiod.sh 2>&1\n" ${daemon_user} ${daemon_dir} > run
chmod 0755 run || exit 255
mkdir log || exit 255
chmod 02755 log || exit 255
mkdir log/main || exit 255
chmod 02755 log/main || exit 255
chown ${log_user}.${log_group} log/main || exit 255
touch log/status || exit 255
chmod 0644 log/status || exit 255
chown ${log_user}.${log_group} log/status || exit 255
printf "#!/bin/sh\nexec setuidgid %s multilog t ./main\n" ${log_user} > log/run
chmod 755 log/run || exit 255

echo "created supervise directory for halo_radio at ${supervize_dir}."
echo

