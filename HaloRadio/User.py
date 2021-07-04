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

import HaloRadio.TopTable as TopTable

class User(TopTable.TopTable):

	"""
	- User -
		pass a userid to instantiate an existing user object.
		pass a 0 for userid, name, email, adminflag to create
		a new user and retun an object.

		The userid 0 is reserved for the system, it means the
		system is responsible for whatever.
	"""

	def __init__( self, id, name=None, password=None, email=None):
		self.tablename = "users"
		id = int(id)
		if id == 0:

			if name == None:
				raise "cannot add a User without a Username."
			id = self.do_my_insert( """INSERT INTO %s SET name=\"%s\", email=\"%s\", password=password(\"%s\"), rights="U", create_time=NOW();""" %
				( self.tablename, name, email, password ) )
		elif id == -1:
			if name==None or password==None:
				raise "cannot authenticate user without a username and a password."
			rows = self.do_my_query(
				"""SELECT id FROM %s WHERE name='%s' AND password=password('%s')""" % (self.tablename, name, password ) )
			try:
				(id, ) = rows[0]
			except:
				raise "Cannot Authenticate User."
			
		"""load up the info for the provided id"""
		rows = self.do_my_query( """SELECT name,email,rights,requests,kills,create_time,style FROM %s WHERE id=%d;""" % ( self.tablename, id ) )
		try:
			(self.name, self.email, self.rights, self.requests, self.kills, self.create_time, style ) = rows[0]
			import HaloRadio.Style as Style
			s = Style.Style(style)
			self.style = s.GetName()
		except IndexError:
			raise "unable to load data for user(%d)" % id

		self.id = id

		return
	def GetDisplayName( self ):
		if self.rights:
			return "%s(%s)" % (self.name,self.rights)
		else:
			return self.name

	def UpdateRequests(self):
		self.do_my_do( """UPDATE %s SET requests=%d WHERE id=%d;""" %
			( self.tablename, self.requests+1, self.id ) )
		self.requests+=1

	def SetPassword(self, newpassword ):
		if newpassword is not None:
			self.do_my_do( """UPDATE %s SET password=password("%s") WHERE id=%d;""" %
				( self.tablename, newpassword, self.id ) )

	def UpdateEmail(self, email="default@halo_radio" ):
		if email is not None:
			self.do_my_do( """UPDATE %s SET email="%s" WHERE id=%d;""" %
				( self.tablename, email, self.id ) )
			self.email = email

	def GetStyle(self):
		return self.style

	def UpdateStyle(self, style ):
		if style is not None:
			self.do_my_do( """UPDATE %s SET style=%d WHERE id=%d;""" %
				( self.tablename, style, self.id ) )
			self.style = style

	def UpdateName(self, username):
		if username is None:
			return
		import HaloRadio.UserListMaker as UserListMaker
		ulm = UserListMaker.UserListMaker()
		ulm.GetByName(username)
		if len(ulm.list) > 0:
			return
		self.do_my_do( """UPDATE %s SET name="%s" WHERE id=%d;""" %
			( self.tablename, username, self.id ) )
		self.name = username

	def UpdateKills(self):
		self.do_my_do( """UPDATE %s SET kills=%d WHERE id=%d;""" %
			( self.tablename, self.kills+1, self.id ) )
		self.kills+=1
		return
	def UpdateRights(self, rights):
		if rights is not None:
			self.do_my_do( """UPDATE %s SET rights="%s" WHERE id=%d;""" % (self.tablename, rights, self.id) )

	def GetNewHash(self):
		import string, random
		newhash=""
		for a in range(0,31):
			newhash+=random.choice(string.hexdigits)
		self.do_my_do( """UPDATE %s SET hash="%s" WHERE id=%d;""" %
			( self.tablename, newhash, self.id ) )
		self.hash=newhash
		return newhash

	def GetHash(self):
		rows = self.do_my_query("""SELECT hash FROM %s WHERE id=%d;""" %
			( self.tablename, self.id ) )
		(hash, ) =rows[0]
		return hash

	def ClearHash(self):
		self.GetNewHash()

	def GetDisplayRights(self):
		import string 
		rows = self.do_my_query("""SELECT rights FROM %s WHERE id=%d;""" %			( self.tablename, self.id ) )
		(rights, ) =rows[0]
		rightlist = []
		for a in range(0,len(rights)):
			rows = self.do_my_query("""SELECT name FROM %s WHERE tag="%s";"""% ( "rights", rights[a] ) )
			(desc, ) = rows[0]
			rightlist.append(desc)

		return string.join(rightlist , ", ")

	def GetRandomSong(self):
		import HaloRadio.Song as Song
		import HaloRadio.Exception as HaloException
		import HaloRadio.UserSongStatsListMaker as UserSongStatsListMaker

		usslm = UserSongStatsListMaker.UserSongStatsListMaker()
		usslm.GetRandomSong(self.id)

		if len(usslm.list) == 1:
			try:
				song = Song.Song(usslm.list[0])
			except HaloException.SongNotFound, snf:
				import HaloRadio.UserSongStats as UserSongStats
				usslm.GetBySong(snf.id)
				for ussid in usslm.list:
					uss = UserSongStats.UserSongStats(ussid)
					uss.Delete()
				song = self.GetRandomSong()
		else:
			return None
		return song
	def GetPostAccess(self):
		rows = self.do_my_query("""SELECT post FROM %s WHERE id=%d;""" % ( self.tablename, self.id ) )
		(access, ) =rows[0]
		return access
	def ChangePostAccess(self):
		if self.GetPostAccess():
			self.do_my_do( """UPDATE %s SET post=%d WHERE id=%d;""" %
				( self.tablename, 0, self.id ) )
		else:
			self.do_my_do( """UPDATE %s SET post=%d WHERE id=%d;""" %
				( self.tablename, 1, self.id ) )
			
	def GetAccess(self):
		rows = self.do_my_query("""SELECT enable FROM %s WHERE id=%d;""" % ( self.tablename, self.id ) )
		(access, ) =rows[0]
		return access
	def ChangeAccess(self):
		if self.GetAccess():
			self.do_my_do( """UPDATE %s SET enable=%d WHERE id=%d;""" %
				( self.tablename, 0, self.id ) )
		else:
			self.do_my_do( """UPDATE %s SET enable=%d WHERE id=%d;""" %
				( self.tablename, 1, self.id ) )
			
	def OldLastSeen(self):
		rows = self.do_my_query( """SELECT active_time FROM session WHERE userid = %d ORDER BY active_time DESC LIMIT 1;""" % self.id)
		try:
			(date, ) = rows[0]
		except:
			return
		return date

	def LastSeen(self):
		rows = self.do_my_query( """SELECT active_time FROM %s WHERE id = %d;""" %(self.tablename,self.id))
		try:
			(date, ) = rows[0]
		except:
			return None
		return date



	def UpdateActivity( self, dt=None ):
		if dt==None:
			self.do_my_do( """UPDATE %s SET active_time=NOW() WHERE id=%d;""" %
				( self.tablename, self.id ))
		else:
			self.do_my_do( """UPDATE %s SET active_time="%s" WHERE id=%d;""" %
				( self.tablename, dt, self.id ))

