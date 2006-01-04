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
import HaloRadio.TopTable as TopTable
import _mysql_exceptions
class UserSongStats(TopTable.TopTable):

	"""
	- UserSongStats -
	mysql> create table user_song_stats ( id INT UNSIGNED auto_increment, songid int UNSIGNED NOT NULL, userid int UNSIGNED NOT NULL, requests smallint UNSIGNED NOT NULL default '0', kills smallint UNSIGNED NOT NULL default '0',PRIMARY KEY  (id), UNIQUE KEY songiduserid (songid, userid))TYPE=MyISAM;
	Query OK, 0 rows affected (0.00 sec)

	"""

	def __init__( self, id, userid=None, songid=None):
		self.tablename = "user_song_stats"
		id = int(id)
		if id == 0:
			if userid == None or songid == None:
				raise "cannot add a UserSongStats without a userid or songid fool."
			try:
				id = self.do_my_insert( """INSERT INTO %s SET userid=%d, songid=%d;""" %
				( self.tablename, userid, songid ) )
			except _mysql_exceptions.IntegrityError, value:
				( errnum, errmsg) = value
				if not errnum==1062:
					raise _mysql_exceptions.IntegrityError, value
				else:
					rows = self.do_my_query( """SELECT id FROM %s WHERE userid=%d and songid=%d""" % ( self.tablename, userid, songid ) )
					(id,) = rows[0]
		"""load up the info for the provided id"""
		rows = self.do_my_query( """SELECT userid,songid,requests,kills FROM %s WHERE id=%d;""" % ( self.tablename, id ) )
		try:
			(self.userid, self.songid, self.requests, self.kills ) = rows[0]
		except IndexError:
			raise "unable to load data for UserSongStats(%d)" % id

		self.id = id

		return

	def UpdateRequests(self):
		self.do_my_do( """UPDATE %s SET requests=%d WHERE id=%d;""" %
			( self.tablename, self.requests+1, self.id ) )
		self.requests+=1
		return 1

	def UpdateKills(self):
		self.do_my_do( """UPDATE %s SET kills=%d WHERE id=%d;""" %
		( self.tablename, self.kills+1, self.id ) )
		self.kills+=1
		return 1
