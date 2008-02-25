#!/usr/bin/python -u

import SimpleXMLRPCServer

#HaloRadio Libraries
import HaloRadio.PlayHistListMaker as PlayHistListMaker

class HaloRPC:
	def __init__(self):
		"""
		"""
		import string
		self.python_string = string

		import HaloRadio
		import HaloRadio.Song as Song
		import HaloRadio.Relay as Relay

		self.config = HaloRadio.conf
		self.configdb = HaloRadio.configdb
		self.hrSong = Song
		self.hrRelay = Relay

	def getCurrentSong(self):
		cursong = int(self.configdb.GetConfigItem("current_song"))
		if cursong == 0:
			currelay = int(self.configdb.GetConfigItem("current_relay"))
			r = self.hrRelay.Relay(currelay)
			return r.GetDisplayName()
		else:
			s = self.hrSong.Song(cursong)
			return s.GetDisplayName()

server = SimpleXMLRPCServer.SimpleXMLRPCServer(("*", 7014))
server.register_instance(HaloRPC())
server.serve_forever()

