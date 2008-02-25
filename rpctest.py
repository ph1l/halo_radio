#!/usr/bin/python
import xmlrpclib

server = xmlrpclib.Server('http://localhost:7014')
print server.getCurrentSong()

