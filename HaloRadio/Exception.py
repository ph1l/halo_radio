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

class Fuck(Exception):
	"""
	This is my exception class ?
	"""

	def __init__(self,  value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class SongNotFound(Exception):
	"""
	This an exception class !
	"""

	def __init__(self,  value=0):
		self.id = value
	def __str__(self):
		return repr(self.value)

class PlaylistEmpty(Exception):
	"""
	This an exception class !
	"""

	def __init__(self,  value):
		self.id = value
	def __str__(self):
		return repr(self.value)

class RequestOverQuota(Exception):
	"""
	This an exception class !
	"""

	def __init__(self,  value):
		self.value = value
	def __str__(self):
		return "Request by User (%s) over Quota" % (self.value)

class RequestOverPlayed(Exception):
	"""
	This an exception class !
	"""

	def __init__(self,  value):
		self.value = value
	def __str__(self):
		return "Request by User (%s) over played" % (self.value)

class SongNotExistant(Exception):
	"""
	"""

	def __init__(self,  value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class RequestNotFound(Exception):
	"""
	This an exception class !
	"""

	def __init__(self,  value):
		self.id = value
	def __str__(self):
		return repr(self.value)

class InvalidInput(Exception):
	"""
	This an exception class !
	"""

	def __init__(self,  value):
		self.id = value
	def __str__(self):
		return "Invalid Input: %s" % (self.value)

