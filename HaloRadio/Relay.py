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

class Relay(TopTable.TopTable):
	"""
	- Relay -
	This class is for working with a relay.

		a relay object must be passed a relayid.
	"""

	def __init__( self, id, url="", title="", comment="" ):
		self.tablename = "relays"
		id = int(id)
		if id == 0:
			"""insert a new relay and return a relay object."""

			if url == "":
				raise "cannot add a relay without a url."
			id = self.do_my_insert( """INSERT INTO relays SET url="%s", title="%s", comment="%s", added_date=NOW();""" %
				( self.escape(url),self.escape(title), self.escape(comment)) )
			self.id = id
			#self.UpdateAddedDate()
			
			
		"""load up the info for the provided id"""
		rows = self.do_my_query( """SELECT url,title,comment,added_date,plays,requests,kills FROM relays WHERE id=%d;""" % ( id ) )
		try:
			( self.url, self.title, self.comment, self.added_date, self.plays, self.requests, self.kills) = rows[0]
		except IndexError:
			import HaloRadio.Exception as Exception
			raise Exception.RelayNotFound, id

		self.id = id


		return

	def GetDisplayName( self ):
		"""
		- Relay.GetDisplayName -
			get a nice string describing the relay.

		Returns:
			a string
		"""
		import string
		if self.title == "":
			returnstr = self.url
		else:
			returnstr = self.title
		returnstrclean=""
		for i in range(0,len(returnstr)):
			if returnstr[i] in string.printable:
				returnstrclean += returnstr[i]

		
		return returnstrclean


	def GetCleanDisplayName( self ):
		"""
		- Relay.GetCleanDisplayName -
			get a nice string describing the relay.

		Returns:
			a string
		"""
		
		return self.GetDisplayName()

	def Play(self,requestby=0):
		import HaloRadio.PlayHist as PlayHist
		import HaloRadio.Config as Config

		self.do_my_do( """UPDATE relays SET plays=%d WHERE id=%d;""" %
			( self.plays+1, self.id ) )
		cfg = Config.Config()
		cfg.SetConfigItem( "current_song", "r:%s"%(self.id) )

	def UpdateRequests(self):
		self.do_my_do( """UPDATE relays SET requests=%d WHERE id=%d;""" %
			( self.requests+1, self.id ) )

	def UpdateKills(self):
		self.do_my_do( """UPDATE relays SET kills=%d WHERE id=%d;""" %
			( self.kills+1, self.id ) )
