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

	def GetRequest ( self, index ):
		if self.list == []:
			import HaloRadio.Exception as Exception
			raise Exception.SongNotFound
		import HaloRadio.Request as Request
		req = Request.Request( self.list[index])
		return req

        def GetByUser ( self, userid ):
                self.list = [ ]
                query = """requestby = %d """ % ( userid )
                result = self.GetWhere( query )

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

