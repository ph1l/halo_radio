#
#
#    Copyright (C) 2006 Patrick J Freeman
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

import HaloRadio.TopTable as TopTable
class Style(TopTable.TopTable):

	"""
	- Style -
	This Class is for styles. duh.

	"""

	def __init__( self, id ):
		self.tablename = "styles"
		id = int(id)
		if id < 1:
			raise "cannot get a non-existant Style fool."
		"""load up the info for the provided id"""
		rows = self.do_my_query( """SELECT id,style FROM %s WHERE id=%d;""" % ( self.tablename, id ) )
		try:
			(self.id, self.style ) = rows[0]
		except IndexError:
			raise "unable to load data for Style(%d)" % id
		return
        def GetName( self ):
                return self.style
	def GetId( self):
		return self.id
