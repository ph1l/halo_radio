#
#
#    Copyright (C) 2004 Philip J Freeman
#
#    This file is part of halo_radio
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import HaloRadio.TopTable as TopTable

class PlayHist(TopTable.TopTable):

	"""
	- PlayHist -
	This module works with rows from the play history table.
	"""

	def __init__( self, id, songid=0, requestby=0 ):
		self.tablename = "play_history"
		id = int(id)
		if id == 0:
			if songid == 0:
				raise "cannot add a request without a songid."
			id = self.do_my_insert( """INSERT INTO %s SET songid="%d", requestby=%d, date=NOW();""" %
				( self.tablename, songid, requestby) )
			
		"""load up the info for the provided id"""
		rows = self.do_my_query( """SELECT songid, requestby, date FROM %s WHERE id=%d;""" % ( self.tablename, id ) )
		try:
			( self.songid, self.requestby, self.date ) = rows[0]
		except IndexError:
			raise "unable to load data for request(%d)" % id

		self.id = id

		return

	def GetSong( self ):
		import HaloRadio.Song as Song
		song = Song.Song(self.songid)
		return song
