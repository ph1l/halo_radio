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

class SessionListMaker(TopListMaker.TopListMaker):
	"""
	- SessionListMaker -
	"""

	def __init__( self ):
		self.list = [ ]
		self.tablename = 'session'
		return

	def GetSession ( self, index ):
		import HaloRadio.Session as Session
		session = Session.Session(self.list[index])
		return session

	def GetActive ( self, activity_timeout=30 ):
		import time
		timestr=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()-(activity_timeout*60)))
		self.GetWhere( """active_time > "%s" """% (timestr), """active_time DESC""" )

	def GetActiveNotAnonymous ( self, activity_timeout=30 ):
		import time
		timestr=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()-(activity_timeout*60)))
		self.GetWhere( """active_time > "%s" AND userid != 1 """% (timestr), """active_time DESC""" )

