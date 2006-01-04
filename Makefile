
SHARE=/usr/share/haloradio
LOG=/var/log/haloradio
ETC=/etc/haloradio
VAR=/var/lib/haloradio

SCRIPTS=chpasswd.py cron.daily.sh cron.often.sh file_list.py halostatcron.py halostatcron.sh install_web.sh list_songs.py radio-conf.sh radiod.py radiod.sh rename.py HaloRadio.cgi DBSync.py
FILES=compile.sh favicon.ico HaloRadio.ini-dist halo_radio.mysql sendmail.py style.css .htaccess
DIRS=HaloRadio help WebRoot

MP3_COMMERCIALS=halo_radio-commercial-waits-punk-patch.mp3

all:
	echo done.
install:
	mkdir -p $(DESTDIR)$(SHARE)
	mkdir -p $(DESTDIR)$(SHARE)/public_html
	mkdir -p $(DESTDIR)$(LOG)
	mkdir -p $(DESTDIR)$(ETC)
	mkdir -p $(DESTDIR)$(VAR)
	mkdir -p $(DESTDIR)$(VAR)/rrd
	mkdir -p $(DESTDIR)$(VAR)/png
	mkdir -p $(DESTDIR)$(VAR)/mp3
	mkdir -p $(DESTDIR)$(VAR)/mp3/halo_radio
	for FILE in $(MP3_COMMERCIALS); do install -o root -g root -m 644 mp3/halo_radio/$${FILE} $(DESTDIR)$(VAR)/mp3/halo_radio; done
	chown -R radio.radio $(DESTDIR)$(LOG)
	chown -R radio.radio $(DESTDIR)$(ETC)
	chown -R radio.radio $(DESTDIR)$(VAR)
	chmod 750 $(DESTDIR)$(LOG)
	chmod 750 $(DESTDIR)$(ETC)
	chmod 750 $(DESTDIR)$(VAR)
	for FILE in $(SCRIPTS); do install -o root -g root -m 755 $${FILE} $(DESTDIR)$(SHARE); done
	for FILE in $(FILES); do install -o root -g root -m 644 $${FILE} $(DESTDIR)$(SHARE); done
	for DIR in $(DIRS); do mkdir -p $(DESTDIR)$(SHARE)/$${DIR}; for FILE in $${DIR}/*; do install -o root -g root $${FILE} $(DESTDIR)$(SHARE)/$${DIR};done;done
	ln -s /etc/haloradio/HaloRadio.ini $(DESTDIR)$(SHARE)/HaloRadio.ini
	install -o radio -g radio -m 750 HaloRadio.ini-dist $(DESTDIR)$(ETC)/HaloRadio.ini
	( cd $(DESTDIR)$(SHARE)/WebRoot; make clean links )
	( cd $(DESTDIR)$(SHARE); sh install_web.sh public_html )
	chown -R radio.radio $(DESTDIR)$(SHARE)/public_html
