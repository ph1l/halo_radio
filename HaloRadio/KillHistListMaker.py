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

class KillHistListMaker(TopListMaker.TopListMaker):
	"""
	- KillHistListMaker -
	This class is for working with play history lists.
	"""

	def __init__( self ):
		self.tablename = "kill_history"
		self.list = [ ]
		return

	def GetKillHist ( self, index ):
		if self.list == []:
			raise "No Items In List."
		import HaloRadio.KillHist as KillHist
		ph = KillHist.KillHist( self.list[index])
		return ph
