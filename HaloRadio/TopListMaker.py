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
#_______________________________________________________________halo_radio_____
# Title : 
# Author : Philip Freeman
# Description : 
#------------------------------------------------------------------------------

import HaloRadio
import HaloRadio.TopTable as TopTable
import string

import MySQLdb
import _mysql_exceptions


class TopListMaker(TopTable.TopTable):
	"""
	TopListMaker - Parent class for lists of objects in the database.

	"""


	def __init__(self):
		pass

	def Pop( self ):
		item = self.list[0]
		self.list = self.list[1:]
		return item

	def Skip( self, num ):
		for i in range( 0, num):
			self.list = self.list[1:] 
		return


	def Get( self, num=1 ):
		self.list = [ ]
		result = self.do_my_query("SELECT id from %s LIMIT %d" % ( self.tablename, num) )	     
		for row in result:
			(id, ) = row
			self.list.append(id)
		return

	def GetAll( self ):
		self.list = [ ]
		result = self.do_my_query("SELECT id from %s" % ( self.tablename) )	     
		for row in result:
			#ValueError: unpack tuple of wrong size
			try:
				(id, ) = row
				self.list.append(id)
			except ValueError:
				pass
		return

	def GetWhere ( self, where_str, order_str="" ):
		self.list = [ ]
		query = """SELECT id from %s """ % ( self.tablename )
		if where_str != "":
			query += " WHERE " + where_str
		if order_str != "":
			query += " ORDER BY " + order_str + " "
		query += " ;"
		result = self.do_my_query( query )
		for row in result:
			(id, ) = row
			self.list.append(id)
		return
	def GetRecent ( self, num=3 ):
		self.list = [ ]
                query = """ SELECT id FROM %s ORDER BY date DESC LIMIT %d """ % ( self.tablename,num )
		result = self.do_my_query( query )
		for row in result:
			(id, ) = row
			self.list.append(id)
		return
