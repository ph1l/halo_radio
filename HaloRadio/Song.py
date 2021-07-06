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

class Song(TopTable.TopTable):
	"""
	- Song -
	This class is for working with a song.

		a song object must be passed a songid.
	"""

	def __init__( self, id, path="", artist="", album="", title="", track=0, genre="", comment="", year="", mime=0, samplerate=0, length=0 ):
		self.tablename = "songs"
		id = int(id)
		if id == 0:
			"""insert a new song and return a song object."""

			if path == "":
				raise "cannot add a song without a path."
			id = self.do_my_insert( """INSERT INTO songs SET path="%s", artist="%s", album="%s", title="%s", track=%d, genre="%s", comment="%s", year="%s",mime="%s", samplerate=%r, length=%d;""" %
				( self.escape(path), self.escape(artist), self.escape(album), self.escape(title), track, self.escape(genre), self.escape(comment), self.escape(year), self.escape(mime), samplerate, length ) )
			self.id = id
			self.UpdateAddedDate()
			
			
		"""load up the info for the provided id"""
		rows = self.do_my_query( """SELECT path,artist,album,title,track,genre,comment,year,mime,samplerate,length,requests,plays,kills,added_date,scale FROM songs WHERE id=%d;""" % ( id ) )
		try:
			( self.path, self.artist, self.album, self.title, self.track, self.genre, self.comment, self.year, self.mime, self.samplerate, self.length, self.requests, self.plays, self.kills, self.added_date, self.scale ) = rows[0]
		except IndexError:
			import HaloRadio.Exception as Exception
			raise Exception.SongNotFound, id

		self.id = id


		return
	def Update( self, artist="", album="", title="", track=0, genre="", comment="", year="", mime="", samplerate=0,  length=0 ):
		querystr = """UPDATE songs SET artist="%s", album="%s", title="%s", track=%d, genre="%s", comment="%s", year="%s",mime="%s", samplerate=%r, length=%d WHERE id="%d";""" % ( self.escape(artist), self.escape(album), self.escape(title), track, self.escape(genre), self.escape(comment), self.escape(year),self.escape(mime),samplerate,length, self.id )
		#print querystr
		self.do_my_do(querystr) 
		self.artist=artist
		self.album=album
		self.title=title
		self.track=track
		self.genre=genre
		self.comment=comment
		self.year=year
		self.mime=mime
		self.samplerate=samplerate
		self.length=length
		return
	

	def GetDisplayLength( self ):
		"""
		- Song.GetDisplayTime - 
		"""
		if self.length == 0:
			return "??:??"
		else:
			return "%02d:%02d" % (
				self.length / 60,
				self.length % 60 )
		
	def GetDisplayName( self ):
		"""
		- Song.GetDisplayName -
			get a nice string describing the song.

		Returns:
			a string
		"""
		import string
		returnstr = ""
		if ( self.artist != "" and self.title != "" ):
			if ( self.album != "" ):
				if ( self.track != 0 ):
					al = "%s #%02d" % ( self.album, self.track )
				else:
					al = self.album
				returnstr = "%s - %s - %s" % ( self.artist, al, self.title )
			else:
				returnstr = "%s - %s" % ( self.artist, self.title )
		else:
			returnstr = self.path
		returnstrclean=""
		for i in range(0,len(returnstr)):
			if returnstr[i] in string.printable:
				returnstrclean += returnstr[i]

		
		return returnstrclean


	def GetCleanDisplayName( self ):
		"""
		- Song.GetCleanDisplayName -
			get a nice string describing the song.

		Returns:
			a string
		"""
		
		import string, re

		if ( self.artist != "" and self.title != "" ):
			outstring = "%s-%s" % ( self.artist, self.title )
		else:
			fields = string.split(self.path,"/")
			outstring = fields[len(fields)-1]
		search=1
		index=0
		junkmatch = re.compile(r'[_\W]+')
		while search==1:
			target = junkmatch.search(outstring, index)
			if target == None:
				return outstring
			index = target.start()+1
			outstring = outstring[:target.start()] + "_" + outstring[target.end():]


	def Play(self,requestby=0):
		import HaloRadio.PlayHist as PlayHist
		import HaloRadio.Config as Config

		self.do_my_do( """UPDATE songs SET plays=%d WHERE id=%d;""" %
			( self.plays+1, self.id ) )
		ph = PlayHist.PlayHist(0,self.id,requestby)
		cfg = Config.Config()
		cfg.SetConfigItem( "current_song", str(self.id) )

	def UpdateRequests(self):
		self.do_my_do( """UPDATE songs SET requests=%d WHERE id=%d;""" %
			( self.requests+1, self.id ) )

	def UpdateKills(self):
		self.do_my_do( """UPDATE songs SET kills=%d WHERE id=%d;""" %
			( self.kills+1, self.id ) )

	def UpdatePath(self, path):
		self.do_my_do( """UPDATE songs SET path="%s" WHERE id=%d;""" %
			( path, self.id ) )
		self.path=path

	def UpdateAddedDate(self):
		import time
		self.added_date = time.strftime("%Y-%m-%d %H:%M:%S")
		self.do_my_do( """UPDATE songs SET added_date="%s" WHERE id=%d;""" %
			( self.added_date, self.id ) )

	def UpdateScale(self, scale):
		try:
			scale=float(scale)
		except ValueError:
			scale=0
		self.do_my_do( """UPDATE songs SET scale=%s WHERE id=%d;""" %
			( scale, self.id ) )
		self.scale = scale

	def GetNumRecentRequests( self, days=7):
		query="""SELECT count(songid) as number from play_history where songid=%d AND requestby != 0 AND date>FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d) GROUP BY songid;""" % (self.id,days*24*60*60)
		result = self.do_my_query( query )
		try:
			return result[0][0]
		except:
			return 0

	def GetNumRecentKills( self, days=7):
		query="""SELECT count(songid) as number from kill_history where songid=%d AND killby != 0 AND date>FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d) GROUP BY songid;""" % (self.id,days*24*60*60)
		result = self.do_my_query( query )
		try:
			return result[0][0]
		except:
			return 0

	def GetRequestsFromUsers( self, users, recent=0 ):
		if recent > 0:
			query="""SELECT count(songid) as number from play_history where songid=%d AND requestby in (%s) AND play_history.date > FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d) GROUP BY songid;""" % ( self.id, users, (recent*24*60*60) )
		else:
			query="""SELECT count(songid) as number from play_history where songid=%d AND requestby in (%s) GROUP BY songid;""" % ( self.id, users )
		result = self.do_my_query( query )
		try:
			return result[0][0]
		except:
			return 0

	def GetKillsFromUsers( self, users, recent=0 ):
		if recent > 0:
			query="""SELECT count(songid) as number from kill_history where songid=%d AND killby in (%s) AND kill_history.date > FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d) GROUP BY songid;""" % ( self.id, users, (recent*24*60*60) )
		else:
			query="""SELECT count(songid) as number from kill_history where songid=%d AND killby in (%s) GROUP BY songid;""" % ( self.id, users )
		result = self.do_my_query( query )
		try:
			return result[0][0]
		except:
			return 0

