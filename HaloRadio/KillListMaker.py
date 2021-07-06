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
import HaloRadio.Exception as Exception

class KillListMaker(TopListMaker.TopListMaker):
	"""
	- KillListMaker -
	This Class is for getting and orking with lists of kills.
	"""

	def __init__( self ):
		self.tablename = "kill_queue"
		self.list = [ ]
		return

	def GetKills ( self ):
		import HaloRadio.Kill as Kill

		if self.list == [ ]:
			self.GetAll()
		outlist = [ ]
		for killid in self.list:
			outlist.append( Kill.Kill(killid) )
		return outlist
