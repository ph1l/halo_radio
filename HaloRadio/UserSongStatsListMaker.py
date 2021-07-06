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

import HaloRadio.TopListMaker as TopListMaker
import HaloRadio.Exception as HaloException
import re

class UserSongStatsListMaker(TopListMaker.TopListMaker):
	"""
	- UserSongStatsListMaker -
	"""

	def __init__( self ):
		self.list = [ ]
		self.tablename = 'user_song_stats'
		return

	def GetRandomSong ( self, userid ):
		self.list = [ ]
		query = """SELECT songid FROM %s WHERE userid='%d' and requests > kills ORDER BY rand() DESC LIMIT 1""" % ( self.tablename, userid )
		result = self.do_my_query( query )
		for row in result:
			(id, ) = row
			self.list.append(id)
		return
	def GetBySong ( self, songid ):
		self.list = [ ]
		query = """SELECT id FROM %s WHERE songid="%s";"""%(self.tablename, songid )
		result = self.do_my_query( query )
		for row in result:
			(id, ) = row
			self.list.append(id)
		return

	def GetTopRank ( self, userid, num ):
		self.list = [ ]
		query = """SELECT songid, requests, kills FROM %s WHERE userid='%d' AND requests> kills > 0 ORDER BY requests DESC LIMIT %d""" % ( self.tablename, userid, num )
		result = self.do_my_query( query )
		for row in result:
			(id, requests, kills) = row
			self.list.append((id, requests, kills))
		return

	def GetBottomRank ( self, userid, num ):
		self.list = [ ]
		query = """SELECT songid, kills, requests FROM %s WHERE userid=%d ORDER BY kills - requests DESC LIMIT %d""" % ( self.tablename, userid, num )
		
		result = self.do_my_query( query )
		for row in result:
			(id, kills, requests) = row
			self.list.append((id, kills, requests))
		return

        def GetRandomSongForUsers ( self, useridlist ):
                import HaloRadio.Song as Song

		wheres = []
                for userid in useridlist:
                        wheres.append(" userid = \"%s\" "%userid)

                query = """SELECT SUM(requests) as requests, SUM(kills) as kills, (rand()*100) as rank, songid FROM %s WHERE %s GROUP BY songid HAVING requests > kills ORDER BY rank DESC LIMIT 1;""" % (self.tablename, " OR ".join(wheres) )
                try:
			((requests, kills, rank, songid),) = self.do_my_query( query )
		except ValueError:
			raise HaloException.SongNotExistant
                try:
                        song = Song.Song(songid)
                except HaloException.SongNotFound, snf:
                        song = self.GetRandomSongForUsers(useridlist)
                return song

