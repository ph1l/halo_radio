#!/usr/bin/python -u
# 
# radiod - This is the stream source.
#    Copyright (C) 2004 Philip J Freeman
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
#

import time, os, fcntl, select, tempfile, stat, sys, signal


def logger( strg ):
	print strg



fifopath=tempfile.mktemp()
logger("tempfile for fifo: %s"% (fifopath))

try:
	os.unlink(fifopath)
except OSError:
	logger("unable to unlink fifo: %s"% (fifopath))
	pass

os.mkfifo(fifopath)
logger("fifo made.")


logger("forking...")
ppid = os.getpid()
cpid = os.fork()
logger("other side of the fork. pid=%d"%(cpid))
if cpid:
	logger("%d:kill parent starting..." % (ppid))
	import re
	import HaloRadio
	import HaloRadio.PlayLogic as PlayLogic

	tempfile.template = None

	find_state = re.compile("^state:\s+(\w)",re.IGNORECASE)
	pl = PlayLogic.PlayLogic()
	pipew = os.open(fifopath,os.O_WRONLY)
        logger ("setting up signal handlers...")
        def shutdown_handler(signum, frame):
		logger( "Signal handler called with signal: %s"%(signum) )
		logger( "shutting down...")
		try:
			os.write(pipew,"d")
			logger("sent shutdown to shout child")
		except:
			logger("unable to send shutdown to shout child")
		logger("waiting for child to die")
		time.sleep(5)
		try:
			os.unlink(fifopath)
			logger("unlinked fifo: %s"% (fifopath))
		except:
			logger("unable to unlink fifo: %s"% (fifopath))
		sys.exit(0)

	for sig in (signal.SIGHUP, signal.SIGQUIT, signal.SIGKILL, signal.SIGTERM):
		signal.signal(sig, shutdown_handler)
	while 1:
		time.sleep(3)
		i = pl.GetKillState()
		#logger("%d:kill GetKillState retrned %d" % (ppid,i))

		if i == 1:
			logger("%d:kill Kill Found in database. Sending signal to parent." %(ppid))
			try:
				os.write(pipew,"k")
			except OSError:
				pipew = os.open(fifopath,os.O_WRONLY)
				os.write(pipew,"k")
		childprocstat = "/proc/%d/status"%(cpid)
		try:
			mode = os.stat(childprocstat)[stat.ST_MODE]
		except OSError:
			logger("%d:kill shout child went away ? shutting down.." %(ppid))
			sys.exit(255)
		if stat.S_ISREG(mode):
			stat_file = open(childprocstat)
			state = ""
			for line in stat_file.readlines():
				match = find_state.match(line)
				if match != None:
					state = match.group(1)
			if state == "":
				logger("%d:kill couldn't get state from %s." % (ppid, childprocstat) )
			elif state == "Z":
				logger("%d:kill child state is zombie. shutting down.."%(ppid))
				sys.exit(255)
			#else:
			#	logger("%d:kill child state is %s ." % (ppid,state) )
		
else:

	"""
	Shout Child -
	  This part streams the mp3's to the icecast server.
	"""
	import shout
	import time, string
	import HaloRadio
	import HaloRadio.PlayLogic as PlayLogic
	import HaloRadio.Config as Config

	cpid = os.getpid()
	logger("%d:shout child starting..."%(cpid))
	arc_root=HaloRadio.conf['path.root']
	mount=HaloRadio.conf['shout.mount']

	logger("Using libshout version %s" % shout.version())

	piper = os.open(fifopath, os.O_NONBLOCK)
	flags = fcntl.fcntl (piper, fcntl.F_GETFL, 0)
	flags = flags | os.O_NONBLOCK
	fcntl.fcntl (piper, fcntl.F_SETFL, flags)
	pollchild = select.poll()
	pollchild.register(piper, select.POLLIN)

	clonerates=string.split(HaloRadio.conf['shout.bitrate'],",")
	streams = {}
	for br in clonerates:
	    streams[br]={}
	    s = shout.Shout()

	    s.host = HaloRadio.conf['shout.host']
	    s.port = int(HaloRadio.conf['shout.port'])
	    s.user = HaloRadio.conf['shout.user']
	    s.password = HaloRadio.conf['shout.password']
	    s.mount = "%s_%s" % ( HaloRadio.conf['shout.mount'], br)
	    s.format = 'mp3'
	    s.name = HaloRadio.conf['shout.name']
	    s.genre = HaloRadio.conf['shout.genre']
	    s.url = HaloRadio.conf['general.cgi_url']
	    s.public = int(HaloRadio.conf['shout.public'])
	    #  (keys are shout.SHOUT_AI_BITRATE, shout.SHOUT_AI_SAMPLERATE,
	    #   shout.SHOUT_AI_CHANNELS, shout.SHOUT_AI_QUALITY)
	    s.audio_info = { 'shout.SHOUT_AI_BITRATE': br,
		'shout.SHOUT_AI_SAMPLERATE': '44100',
		'shout.SHOUT_AI_CHANNELS': '2',
		}
	    logger("%d:shout connecting to %s:%d on mountpoint %s" % (cpid,s.host,s.port,s.mount))
	    try:
	    	s.open()
	    except shout.ShoutException, errmsg:
	        logger("%d:shout connection failed: %s" % (cpid, errmsg))
	        sys.exit(255)
	    streams[br]['shout']=s


	    

	pl = PlayLogic.PlayLogic()

	cfg = Config.Config()

	while 1:
		logger("%d:shout in logic loop..."%(cpid))
		total = 0
		curs = int(cfg.GetConfigItem("current_song"))
		curr = int(cfg.GetConfigItem("current_relay"))
		if curr !=0:
			import HaloRadio.Relay as Relay
			r = Relay.Relay(curr)
			logger("%d:going into relay mode (%s/%s/%s)..."%(cpid,r.id,r.title,r.url))
			cfg.SetConfigItem("current_song","0")
			curs = int(cfg.GetConfigItem("current_song"))
			for br in streams.keys():
			    s = streams[br]['shout']
			    try:
			        s.set_metadata({'song': r.GetDisplayName()})
			    except:
				logger("%d:error setting metadata %s."%(cpid,r.GetDisplayName()))
			    cmd="wget -O- --quiet \"%s\" | lame --resample 44.1 --mp3input -t --silent -f -b %s - -"%(r.url,br)
			    logger("%d:%s"%(cpid,cmd))
			    streams[br]['child_stdout'] = os.popen( cmd,'r',)
			    streams[br]['nbuf'] =  streams[br]['child_stdout'].read(int(br)*32)


		else:
			song = pl.GetNextSong()
			logger("%d:shout playing %d:%s" % ( cpid,song.id, song.path) )
			oldpercent = 0
			cfg.SetConfigItem("current_percent","0")
			starttime=time.time()
			#
			#
			
			for br in streams.keys():
			    s = streams[br]['shout']
			    try:
			        s.set_metadata({'song': song.GetDisplayName()})
			    except:
				logger("%d:error setting metadata %s."%(cpid,song.GetDisplayName()))
	
			    rate = song.mpeg_samplerate
			    if song.scale == 0:
			    	scale=1
			    else:
			    	scale=song.scale
			    #if rate != 44100:
			    #	cmd = "lame --resample 44.1 --mp3input -t --silent --scale %s -f -b %d \"%s/%s\" - " % ( scale, int(br),arc_root, song.path)
			    #else:
			    cmd = "lame --resample 44.1 --mp3input -t --silent --scale %s -f -b %d \"%s/%s\" - " % ( scale, int(br),arc_root, song.path)
			    logger("%d:%s"%(cpid,cmd))
			    streams[br]['child_stdout'] = os.popen( cmd,'r',)
			    streams[br]['nbuf'] =  streams[br]['child_stdout'].read(int(br)*32)
			    #if song.scale == 0:
			    #    # stat the file to find volume offset
			    #    # DISABLED because it breaks paul's songs.
       		            #    # cmd = "nice sox \"%s/%s\" -t nul /dev/null stat -v 2>&1"%(arc_root,song.path)
			    #    logger("%d:%s"%(cpid,cmd))
			    #    stat_stdout = os.popen( cmd,'r',)

		data = None

		#print repr(streams[br])
		while 1:
			break_now=0
			for br in streams.keys():
			    try:
			      streams[br]['buf'] = streams[br]['nbuf']
			      streams[br]['nbuf'] = streams[br]['child_stdout'].read(int(br)*32)
			    except:
			      pass
			    total = total + len(streams[br]['buf'])
			    if len(streams[br]['buf']) == 0:
				logger("%d:shout empty streams[%s][buf]. total sent %d."%(cpid,br,total))
				break_now=1
				break
			    streams[br]['shout'].send(streams[br]['buf'])
			    streams[br]['shout'].sync()
			if break_now:
				break

			if curr == 0:
				currenttime = time.time()
				percent = (int(int( ((currenttime-starttime)/song.mpeg_length)*100)/2)*2 )
				if percent != oldpercent:
					#logger("%d:shout song %d percent complete"%(cpid,percent))
					cfg.SetConfigItem("current_percent","%d"%percent)
					oldpercent = percent
			else:
				curr = int(cfg.GetConfigItem("current_relay"))
				if curr == 0:
					logger("%d:shout killing relay.."%(cpid))
					for br in streams.keys():
					    streams[br]['child_stdout'].close()
					if curr != 0 and curs == 0:
					    cfg.SetConfigItem("current_relay","0")
					break_now=1
					break
			polllist = pollchild.poll(10)
			if len(polllist) > 0:
				(fd,fd2) = polllist[0]
				data = os.read(fd,1)
			if data == "k":
				data = None
				logger("%d:shout got kill from parent. Killing."%(cpid))
				for br in streams.keys():
				    streams[br]['child_stdout'].close()
				if curr != 0 and curs == 0:
				    cfg.SetConfigItem("current_relay","0")
				break
			if data == "d":
			        data = None
				logger("%d:shout got shutdown from parent..."%(cpid))
				for br in streams.keys():
				    streams[br]['child_stdout'].close()
				sys.exit(0)
			#if song.scale == 0:
			#    import re
			#    stat_out = stat_stdout.readline()
			#    while stat_out != '':
			#        r = re.compile('(\d+\.\d+)')
			#        m = r.match(stat_out)
			#        if m:
			#   	    song.UpdateScale(m.group(1))
			#	    logger("%d:shout got vol of %s"%(cpid,m.group(1)))
			#        stat_out = stat_stdout.readline()
			#    stat_stdout.close()
		for br in streams.keys():
			streams[br]['child_stdout'].close()
			if curr != 0 and curs == 0:
				cfg.SetConfigItem("current_relay","0")

