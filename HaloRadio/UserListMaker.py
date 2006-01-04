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
