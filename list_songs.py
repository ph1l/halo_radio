#!/usr/bin/python

#
# list_songs.py - lists all songs in the database.
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
#

"""
This is a simple script to list all the songs in your database.
"""

import HaloRadio
import HaloRadio.Song as Song
import HaloRadio.SongListMaker as SongListMaker

sl=SongListMaker.SongListMaker()
sl.GetAll()

for id in sl.list:
	s=Song.Song(id)
	print "%d | %s" % ( s.id, s.GetDisplayName() )

print "%d records listed." % len(sl.list)

