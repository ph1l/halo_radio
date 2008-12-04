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

class PlayHistListMaker(TopTable.TopTable):
	"""
	- PlayHistListMaker -
	This class is for working with play history lists.
	"""

	def __init__( self ):
		self.tablename = "play_history"
		self.list = [ ]
		return

	def GetLastPlayForUser ( self, userid ):
		self.list = [ ]
		query = """ SELECT id FROM %s WHERE requestby=%d ORDER BY date DESC LIMIT 1 """ % ( self.tablename,userid )
		result = self.do_my_query( query )
		for row in result:
			(id, ) = row
			self.list.append(id)
		return

	def GetRecentPlays ( self, num=3 ):
		self.list = [ ]
		query = """ SELECT id FROM %s ORDER BY date DESC LIMIT %d """ % ( self.tablename,num )
		result = self.do_my_query( query )
		for row in result:
			(id, ) = row
			self.list.append(id)
		return

	def GetPlayHist ( self, index ):
		if self.list == []:
			raise "No Items In List."
		import HaloRadio.PlayHist as PlayHist
		ph = PlayHist.PlayHist( self.list[index])
		return ph

        def GetRecentForTime ( self, min=60):
                self.list=[]
                query="""SELECT id from %s where date>FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d);"""%(self.tablename,min*60)
                result = self.do_my_query( query )
                for row in result:
                        (id,) = row
                        self.list.append(id)
                return

