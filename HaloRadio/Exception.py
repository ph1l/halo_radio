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

	def __init__(self,  value):
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

