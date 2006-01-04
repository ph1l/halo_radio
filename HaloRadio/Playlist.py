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
import random



class Playlist(TopTable.TopTable):
	"""
	- Playlist -
	"""

	def __init__( self, id, name="" ):
		self.tablename = "playlists"
		self.list = []
		id = int(id)
		if id == 0:
			"""insert a new playlist and return a song object."""

			if name == "":
				raise "cannot add a playlist without a name."
			id = self.do_my_insert( """INSERT INTO %s SET name="%s";""" % ( self.tablename, name ) )
			
		"""load up the info for the provided id"""

		rows = self.do_my_query( """SELECT name FROM %s WHERE id=%d;""" % ( self.tablename, id ) )
		try:
			( self.name, ) = rows[0]
		except IndexError:
			raise "unable to load data for playlist(%d)" % id

		self.id = id

		return


	def GetDisplayName( self ):
		"""
		- Song.GetDisplayName -
			get a nice string describing the song.

		Returns:
			a string
		"""
		return self.name

	def GetList( self ):
		"""
		- Playlist.GetList -
		"""

		self.list = []
		rows = self.do_my_query( """SELECT songid FROM playlistitems WHERE playlistid=%d;""" % ( self.id ) )
		for row in rows:
			( sid, ) = row
			self.list.append(sid)
		
		return
		
	def GetLength( self ):
		"""
		- Playlist.GetLength -
		"""

		rows = self.do_my_query( """SELECT count(*) FROM playlistitems WHERE playlistid=%d;""" % ( self.id ) )
		( self.length, ) = rows[0]
		return self.length
		
	def Clear( self ):

		self.do_my_do( """DELETE FROM playlistitems WHERE playlistid="%d";""" % ( self.id ) )
		return

	def AddSong( self, songid ):
		# this is wierd. commenting out to see if it breaks
		#try:
		self.do_my_do( """INSERT INTO playlistitems SET playlistid="%d", songid="%d";""" % ( self.id, songid ) )
		#except _mysql_exceptions.IntegrityError:
		#	pass
	def DelSong( self, songid ):
		# this is wierd. commenting out to see if it breaks
		#try:
		self.do_my_do( """DELETE FROM playlistitems WHERE playlistid="%d" AND songid="%d";""" % ( self.id, songid ) )
		#except _mysql_exceptions.IntegrityError:
		#	pass
	def GetSong( self, index ):
		import HaloRadio.Song as Song
		song = Song.Song(self.list[index])
		return song

	def GetRandomSong( self ):
		import HaloRadio.Song as Song
		self.GetList()
		if len(self.list) < 1:
			import HaloRadio.Exception as Exception
			raise Exception.PlaylistEmpty, self.id
		song = Song.Song(self.list[random.randint(0,len(self.list)- 1)])
		return song
