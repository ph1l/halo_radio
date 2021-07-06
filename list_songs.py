#!/usr/bin/python

#
# list_songs.py - lists all songs in the database.
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

