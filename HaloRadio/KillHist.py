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

class KillHist(TopTable.TopTable):

	"""
	- KillHist -
	This module works with rows from the kill history table.
	"""

	def __init__( self, id, songid=0, killby=0 ):
		self.tablename = "kill_history"
		id = int(id)
		if id == 0:
			if songid == 0:
				raise "cannot add a kill without a songid."
			id = self.do_my_insert( """INSERT INTO %s SET songid="%d", killby=%d, date=NOW();""" %
				( self.tablename, songid, killby) )
			
		"""load up the info for the provided id"""
		rows = self.do_my_query( """SELECT songid, killby, date FROM %s WHERE id=%d;""" % ( self.tablename, id ) )
		try:
			( self.songid, self.killby, self.date ) = rows[0]
		except IndexError:
			raise "unable to load data for (%d)" % id

		self.id = id

		return

	def GetSong( self ):
		import HaloRadio.Song as Song
		song = Song.Song(self.songid)
		return song
	def GetUser( self ):
		import HaloRadio.User as User
		user = User.User(self.killby)
		return user
