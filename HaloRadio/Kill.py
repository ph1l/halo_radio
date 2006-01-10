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

class Kill(TopTable.TopTable):

	"""
	- Kill -
	The Kill class is to work with individual rows in the kill list.
	Mostly this will be for adding kills to the queue.
	"""

	def __init__( self, id, songid=0, requestby=1 ):
		self.tablename = "kill_queue"
		id = int(id)
		if id == 0:
			"""insert a new song and return a song object."""

			#if songid == 0:
			#	raise "cannot add a kill without a songid."
			id = self.do_my_insert( """INSERT INTO %s SET songid="%d", requestby=%d;""" %
				( self.tablename, songid, requestby) )
		"""load up the info for the provided id"""
		rows = self.do_my_query( """SELECT songid, requestby FROM %s WHERE id=%d;""" % ( self.tablename, id ) )
		try:
			( self.songid, self.requestby ) = rows[0]
		except IndexError:
			raise "unable to load data for request(%d)" % id

		self.id = id

		return

	def GetSong ( self ):
		import HaloRadio.Song as Song
		song = Song.Song(self.songid)
		return song

