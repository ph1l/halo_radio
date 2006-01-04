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

class Config(TopTable.TopTable):
	"""
	- Class Config -
	This class provides an interface to the config table in the
	database.
	"""

	def __init__( self ):
		self.tablename = "config"
		pass

	def GetConfigItem( self, name ):
		"""
		"""
		rows = self.do_my_query( """SELECT data FROM %s WHERE name="%s";""" % ( self.tablename, self.escape(name) ) )
		try:
			( data, ) = rows[0]
		except:
			raise "Error finding Config item (%s)" % (name)

		return data

	def SetConfigItem( self, name, value=""):
		"""
		"""
		self.do_my_query( """UPDATE %s SET data="%s" WHERE name="%s";""" % (self.tablename, self.escape(value), self.escape(name) ) )
		return

	def NewConfigItem( self, name, value=""):
		"""
		"""
		self.do_my_query( """INSERT INTO %s SET data="%s", name="%s";""" % (self.tablename, self.escape(value), self.escape(name) ) )
		return
