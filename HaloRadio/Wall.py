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
import _mysql_exceptions
class Wall(TopTable.TopTable):

	"""
	- Wall -
	This Class is for lines of the Wall. duh.

	"""

	def __init__( self, id, userid=None, line=None):
		self.tablename = "wall"
		id = int(id)
		if id == 0:
			if userid == None or line == None:
				raise "cannot add a Wall without a userid or line fool."
			try:
				id = self.do_my_insert( """INSERT INTO %s SET userid=%d, date=NOW(), line="%s";""" %
				( self.tablename, userid, self.escape(line) ) )
			except _mysql_exceptions.IntegrityError, value:
				( errnum, errmsg) = value
				if not errnum==1062:
					raise _mysql_exceptions.IntegrityError, value
				else:
					rows = self.do_my_query( """SELECT id FROM %s WHERE userid=%d order by date desc """ % ( self.tablename, userid) )
					(id,) = rows[0]
		"""load up the info for the provided id"""
		rows = self.do_my_query( """SELECT userid,date,line FROM %s WHERE id=%d;""" % ( self.tablename, id ) )
		try:
			(self.userid, self.date, self.line ) = rows[0]
		except IndexError:
			raise "unable to load data for Wall(%d)" % id

		self.id = id

		return
        def GetUser( self ):
                import HaloRadio.User as User
                user = User.User(self.userid)
                return user

