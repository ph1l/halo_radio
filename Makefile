PREFIX=/usr

SHARE=$(PREFIX)/share/haloradio
LOG=/var/log/haloradio
ETC=/etc/haloradio
AP_ETC=/etc/apache2/conf.d
VAR=/var/lib/haloradio

#OWNER
USER="radio"
GROUP="radio"

SCRIPTS=chpasswd.py cron.daily.sh cron.often.sh file_list.py halostatcron.py halostatcron.sh install_web.sh list_songs.py radio-conf.sh radiod.py radiod.sh rename.py HaloRadio.cgi DBSync.py HaloRadioRPC.py HaloRadioRPC.sh rpc-conf.sh 
FILES=compile.sh favicon.ico HaloRadio.ini-dist halo_radio.mysql sendmail.py .htaccess html/CurrentInfo.js html/Search.js html/Timeout.html
DIRS=HaloRadio help WebRoot styles

MP3_COMMERCIALS=halo_radio-commercial-waits-punk-patch.mp3

all:
	echo done.
install-pre:
	mkdir -p $(DESTDIR)$(SHARE)
	mkdir -p $(DESTDIR)$(SHARE)/public_html
	mkdir -p $(DESTDIR)$(LOG)
	mkdir -p $(DESTDIR)$(ETC)
	mkdir -p $(DESTDIR)$(AP_ETC)
	mkdir -p $(DESTDIR)$(VAR)
	mkdir -p $(DESTDIR)$(VAR)/rrd
	mkdir -p $(DESTDIR)$(VAR)/mp3
	mkdir -p $(DESTDIR)$(VAR)/mp3/halo_radio
install: install-pre
	chown -R $(USER):$(GROUP) $(DESTDIR)$(LOG)
	chown -R $(USER):$(GROUP) $(DESTDIR)$(ETC)
	chown -R $(USER):$(GROUP) $(DESTDIR)$(VAR)
	for FILE in $(MP3_COMMERCIALS); do install -g root -o root -m 644 mp3/halo_radio/$${FILE} $(DESTDIR)$(VAR)/mp3/halo_radio; done
	for FILE in $(SCRIPTS); do install -o root -g root -m 755 $${FILE} $(DESTDIR)$(SHARE); done
	for FILE in $(FILES); do install -o root -g root -m 644 $${FILE} $(DESTDIR)$(SHARE); done
	for DIR in $(DIRS); do mkdir -p $(DESTDIR)$(SHARE)/$${DIR}; for FILE in $${DIR}/*; do install -o root -g root $${FILE} $(DESTDIR)$(SHARE)/$${DIR};done;done
	install -o root -g root -m 644 apache2-conf.d-haloradio $(DESTDIR)$(AP_ETC)/haloradio

	ln -sf /etc/haloradio/HaloRadio.ini $(DESTDIR)$(SHARE)/HaloRadio.ini
	if [ -e $(DESTDIR)$(ETC)/HaloRadio.ini ]; then install -o $(USER) -g $(GROUP) -m 750 HaloRadio.ini-dist $(DESTDIR)$(ETC)/HaloRadio.ini-dist; else install -o $(USER) -g $(GROUP) -m 750 HaloRadio.ini-dist $(DESTDIR)$(ETC)/HaloRadio.ini; fi
	make install-web
	chown -R $(USER):$(GROUP) $(DESTDIR)$(SHARE)/public_html
	make install-post
install-user: install-pre
	for FILE in $(MP3_COMMERCIALS); do install -m 644 mp3/halo_radio/$${FILE} $(DESTDIR)$(VAR)/mp3/halo_radio; done
	for FILE in $(SCRIPTS); do install -m 755 $${FILE} $(DESTDIR)$(SHARE); done
	for FILE in $(FILES); do install -m 644 $${FILE} $(DESTDIR)$(SHARE); done
	for DIR in $(DIRS); do mkdir -p $(DESTDIR)$(SHARE)/$${DIR}; for FILE in $${DIR}/*; do install $${FILE} $(DESTDIR)$(SHARE)/$${DIR};done;done
	ln -sf $(DESTDIR)$(ETC)/HaloRadio.ini $(DESTDIR)$(SHARE)/HaloRadio.ini
	if [ -e $(DESTDIR)$(ETC)/HaloRadio.ini ]; then install -m 750 HaloRadio.ini-dist $(DESTDIR)$(ETC)/HaloRadio.ini-dist; else install -m 750 HaloRadio.ini-dist $(DESTDIR)$(ETC)/HaloRadio.ini; fi
	make install-web
	make install-post
install-web:
	( cd $(DESTDIR)$(SHARE)/WebRoot; make clean links )
	( cd $(DESTDIR)$(SHARE); sh install_web.sh public_html )
install-post:
	chmod 750 $(DESTDIR)$(LOG)
	chmod 750 $(DESTDIR)$(ETC)
	chmod 750 $(DESTDIR)$(VAR)
	touch $(DESTDIR)$(LOG)/.keep
	touch $(DESTDIR)$(VAR)/.keep
	touch $(DESTDIR)$(VAR)/rrd/.keep
	touch $(DESTDIR)$(VAR)/mp3/.keep
