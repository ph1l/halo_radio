#
#
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
import ConfigParser
import string
import MySQLdb
import _mysql_exceptions


__all__ = [ 'Config', 'MP3Info', 'Playlist', 'Request', 'RequestListMaker', 'Song', 'SongListMaker', 'Util', 'Web' ]

_ConfigDefault = {
}


def LoadConfig( file, config={}):
	config = config.copy()
	cp = ConfigParser.ConfigParser()
	cp.read(file)
	for sec in cp.sections():
		name = string.lower(sec)
		for opt in cp.options(sec):
			config[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
	return config

conf=LoadConfig("HaloRadio.ini", _ConfigDefault)

try:
	db=MySQLdb.connect( host=conf['db.host'],
			db=conf['db.name'],
			user=conf['db.user'],
			passwd=conf['db.pass']
			)
except _mysql_exceptions.OperationalError, (errno, errmsg):
	print "Content-type: text/html\n\nMySQL DB ERROR: %d, %s" % (errno, errmsg)
	import sys
	sys.exit(0)
