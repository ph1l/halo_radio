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
import re

class UserListMaker(TopListMaker.TopListMaker):
	"""
	- UserListMaker -
	"""

	def __init__( self ):
		self.list = [ ]
		self.tablename = 'users'
		return

	def GetUser ( self, index ):
		import HaloRadio.User as User
		user = User.User(self.list[index])
		return user
	def GetByName ( self, name ):
		self.GetWhere( """name="%s" """%(name))
	def GetByEmail ( self, email ):
		self.GetWhere( """email="%s" """%(email))
