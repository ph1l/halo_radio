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
import HaloRadio
import HaloRadio.PlayHistListMaker as PlayHistListMaker
import HaloRadio.Exception as HaloException
import HaloRadio.TopTable as TopTable

class Request(TopTable.TopTable):

	"""
	- Request -
	This class is for making and working with requests.

		pass a 0, a songid, and a userid to instantiate a new
		request object. 
			r = Request.Request(0,songid,1)
	"""

	def __init__( self, id, songid=0, requestby=0 ):
		self.tablename = "request_queue"
		id = int(id)
		if id == 0:
			"""insert a new song and return a song object."""

			if songid == 0:
				raise "cannot add a request without a songid."
			import HaloRadio.SessionListMaker as SessionListMaker
			import HaloRadio.RequestListMaker as RequestListMaker
			rlm = RequestListMaker.RequestListMaker()
			rlm.GetByUser(int(requestby))
			if int(HaloRadio.conf['general.request_quota']) != 0 and len(rlm.list) >= int(HaloRadio.conf['general.request_quota']):
				raise HaloException.RequestOverQuota, requestby
			#
			# Checking Play History
			#

			phlm = PlayHistListMaker.PlayHistListMaker()
			phlm.GetRecentForTime(int(HaloRadio.conf['general.rerequest_limit']))
			for i in range(0,len(phlm.list)):
				ph = phlm.GetPlayHist(i)
				if ph.requestby != 0 and ph.songid == songid:
					raise HaloException.RequestOverPlayed, requestby 
			
			#
			# Checking Request Queue
			#

			rlm = RequestListMaker.RequestListMaker()
			rlm.GetByUserInclHeld(requestby)
			if int(HaloRadio.conf['general.rerequest_limit']) > 0:
				for i in range(0,len(rlm.list)):
					r = rlm.GetRequest(i)
					if r.songid == songid:
						raise HaloException.RequestOverPlayed, requestby
			#
			# Making Request
			#

			id = self.do_my_insert( """INSERT INTO %s SET songid="%d", requestby=%d;""" %
				( self.tablename, songid, requestby) )
			
		"""load up the info for the provided id"""
		rows = self.do_my_query( """SELECT songid, requestby, hold FROM %s WHERE id=%d;""" % ( self.tablename, id ) )
		try:
			( self.songid, self.requestby, self.hold ) = rows[0]
		except IndexError:
			raise HaloException.RequestNotFound("unable to load data for request(%d)" % id)

		self.id = id

		return
	def Update( self, songid, requestby, hold = 0):
		self.do_my_do( """UPDATE %s SET songid="%s", requestby="%s", hold = %d WHERE id=%d;""" %
			( self.tablename, songid, requestby, hold, self.id )
		)
		self.songid = songid
		self.requestby = requestby

	def GetSong ( self ):
		import HaloRadio.Song as Song
		song = Song.Song(self.songid)
		return song

	def Swap ( self, otherid ):
		import HaloRadio.Request as Request
		r2 = Request.Request( otherid )

		saved_songid = self.songid
		saved_reqby = self.requestby
		saved_hold = self.hold

		self.Update(r2.songid, r2.requestby, r2.hold)
		r2.Update(saved_songid, saved_reqby, saved_hold)

	def GetUser( self ):
		import HaloRadio.User as User
		user = User.User(self.requestby)
		return user

	def Lock( self ):
		self.do_my_do('lock table request_queue write')

	def Unlock( self ):
		self.do_my_do('unlock tables')

	def Hold( self ):
		self.do_my_do( """UPDATE %s SET hold = 1 WHERE id = %d;""" %
			( self.tablename, self.id )
		)

	def UnHold( self ):
		self.do_my_do( """UPDATE %s SET hold = 0 WHERE id = %d;""" %
			( self.tablename, self.id )
		)
