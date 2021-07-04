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

class RequestListMaker(TopListMaker.TopListMaker):
	"""
	- RequestListMaker -
	This class is for working with the request list (the queue).
	"""

	def __init__( self ):
		self.tablename = "request_queue"
		self.list = [ ]
		return

	def GetNextRequest ( self ):
		if self.list == []:
			import HaloRadio.Exception as Exception
			raise Exception.SongNotFound
		import datetime, time
		import HaloRadio.Request as Request
		import HaloRadio.SessionListMaker as SessionListMaker
		import HaloRadio.Session as Session
		import HaloRadio.PlayHistListMaker as PlayHistListMaker
		#print "GetNextRequest begin"
		oldest_recent_timestamp=time.time()
		req=None
		# Build a list of currently active users.
		slm=SessionListMaker.SessionListMaker()
		slm.GetActive()
		for sessionid in slm.list:
			session = Session.Session(sessionid)
			#print "GetNextRequest user %d"%(session.userid)
			# get timestamp for last request per user.
			phlm = PlayHistListMaker.PlayHistListMaker()
			phlm.GetLastPlayForUser(session.userid)
			if len(phlm.list) != 1:
				self.GetByUser(session.userid)
				if len(self.list) >0:
					req = Request.Request(self.list[0])
					if req.hold == 0:
						oldest_recent_timestamp=0
					else:
						req = None
				continue
				
			ph = phlm.GetPlayHist(0)
			test_timestamp=time.mktime(ph.date.timetuple())
			#print "GetNextRequest User %d %s/%s "%(session.userid, oldest_recent_timestamp, test_timestamp)
			if test_timestamp < oldest_recent_timestamp:
				self.GetByUser(session.userid)
				#print "GetNextRequest list %d"%(len(self.list))
				if len(self.list) >0:
					req = Request.Request(self.list[0])
					if req.hold == 0:
						oldest_recent_timestamp = test_timestamp
					else:
						req = None
		return req

	def GetRequest ( self, index ):
		if self.list == []:
			import HaloRadio.Exception as Exception
			raise Exception.SongNotFound
		import HaloRadio.Request as Request
		req = Request.Request( self.list[index])
		return req

        def GetByUser ( self, userid ):
                self.list = [ ]
                query = """requestby = %d AND hold = 0 """ % ( userid )
                result = self.GetWhere( query, "id" )

        def GetByUserInclHeld ( self, userid ):
                self.list = [ ]
                query = """requestby = %d """ % ( userid )
                result = self.GetWhere( query, "id" )

	def Get( self, num=1 ):
		self.list = [ ]
		result = self.do_my_query("SELECT id from %s WHERE hold = 0 ORDER BY id ASC LIMIT %d" % ( self.tablename, num) )
		for row in result:
			(id, ) = row
			self.list.append(id)
		return

	def GetAll( self ):
		self.list = [ ]
		result = self.do_my_query("SELECT id from %s WHERE hold = 0 ORDER BY id ASC" % ( self.tablename) )
		for row in result:
			(id, ) = row
			self.list.append(id)
		return

	def GetAllHeld( self ):
		self.list = [ ]
		result = self.do_my_query("SELECT id from %s ORDER BY id ASC" % ( self.tablename) )
		for row in result:
			(id, ) = row
			self.list.append(id)
		return

	def GetHeld( self ):
		result = self.GetWhere( """hold = 1 """ )

	def GetByUserHeld( self, userid ):
		self.list = [ ]
                query = """requestby = %d AND hold = 1 """ % ( userid )
		result = self.GetWhere( query )

