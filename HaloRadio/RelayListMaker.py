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
import re

class RelayListMaker(TopListMaker.TopListMaker):
	"""
	- RelayListMaker -
	"""

	def __init__( self ):
		self.list = [ ]
		self.tablename = 'relays'
		return

	def GetRelay ( self, index ):
		import HaloRadio.Relay as Relay
		relay = Relay.Relay(self.list[index])
		return relay
