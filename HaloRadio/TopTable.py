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
import string

import MySQLdb
import _mysql_exceptions


class TopTable:
	"""
	- Song -
		A Class For Working with songs.
	"""


	def __init__(self):
		pass

	def fixconn( self ):
		HaloRadio.db = MySQLdb.connect( host=HaloRadio.conf['db.host'],
			db=HaloRadio.conf['db.name'],
			user=HaloRadio.conf['db.user'],
			passwd=HaloRadio.conf['db.pass']
			)
		try:
			self.do_my_query("select COUNT(*) from songs;")
		except:
			return 0
		return 1

	def do_my_query( self, query ):
		"""
		"""
		
		sel = HaloRadio.db.cursor()
		try:
			sel.execute(query)
			rows = sel.fetchall()
		except _mysql_exceptions.OperationalError, value:
			#: (2013, 'Lost connection to MySQL server during query')
			( errno, desc ) = value

			print "query=%s, errno=%d, err=%s" % ( query, errno, desc )
			if self.fixconn():
				rows = do_my_query(self, query )
			else :
				raise  _mysql_exceptions.OperationalError, value

		if rows == None:
			raise "didn't get any results for query (%s)" % ( query )
		sel.close()
		return rows
		
	def do_my_insert( self, query ):
		"""
		"""
	       
		ins = HaloRadio.db.cursor()
		try:
			ins.execute(query)
		except _mysql_exceptions.OperationalError, value:
			#: (2013, 'Lost connection to MySQL server during query')
			( errno, desc ) = value

			print "query=%s, errno=%d, err=%s" % ( query, errno, desc )
			raise  _mysql_exceptions.OperationalError, value


		aiid = ins.lastrowid
		ins.close
		return aiid

	def do_my_do( self, query ):
		"""
		"""
	       
		upd = HaloRadio.db.cursor()
		try:
			upd.execute(query)
		except _mysql_exceptions.Warning:
			pass
		except _mysql_exceptions.OperationalError, value:
			#: (2013, 'Lost connection to MySQL server during query')
			( errno, desc ) = value

			print "Content-type: text/html\n\nquery=%s, errno=%d, err=%s" % ( query, errno, desc )
			raise  _mysql_exceptions.OperationalError, value

		upd.close()
		return

	def escape( self, str ):
		"""
		"""
		if str == None:
			return ""
		str = string.replace(str, "\\", "\\\\")
		str = string.replace(str, "\"", "\\\"")
		return str

	def my_esc_like( self, str ):
		"""
		"""
		if str == None:
			return ""
		str = string.replace(str, "\\", "\\\\")
		str = string.replace(str, "\"", "\\\"")
		str = string.replace(str, "_", "\\_")
		str = string.replace(str, " ", "\\ ")
		str = string.replace(str, "%", "\\%")
		return str

	def Delete( self ):
		self.do_my_do( """DELETE FROM %s WHERE id=%d;""" % ( self.tablename, self.id ) )
		return

