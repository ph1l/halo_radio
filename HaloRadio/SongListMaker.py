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
import HaloRadio.TopListMaker as TopListMaker
import re

class SongListMaker(TopListMaker.TopListMaker):
	"""
	- SongListMaker -
	"""

	def __init__( self ):
		self.list = [ ]
		self.tablename = 'songs'
		return

	#def GetAll( self ):
	#	self.list = [ ]
	#	result = self.do_my_query("SELECT id from %s" % ( self.tablename ) )
	#	for row in result:
	#		(id, ) = row
	#		self.list.append(id)
	#	return

	#def GetWhere ( self, where_str ):
	#	self.list = [ ]
	#	query = """SELECT id from %s WHERE """ % ( self.tablename )
	#	query += where_str + " ;"
	#	result = self.do_my_query( query )
	#	for row in result:
	#		(id, ) = row
	#		self.list.append(id)
	#	return

	def GetSong ( self, index ):
		import HaloRadio.Song as Song
		song = Song.Song(self.list[index])
		return song

	def GetTopPlays ( self, num ):
		self.list = [ ]
		query = """SELECT id FROM songs ORDER BY plays DESC LIMIT %d""" % ( num )
		result = self.do_my_query( query )
		for row in result:
			(id, ) = row
			self.list.append(id)
		return

	def SearchPath ( self, query_in ):
		where_str = """ path LIKE "%s" ORDER BY path""" % ( self.my_esc_like(query_in) )
		self.GetWhere( where_str )
		return

	def SubSearchPath ( self, query_in, order="natural" ):
		where_str = ""
		pieces = re.split(r'[ \t]+', query_in)
		for piece in pieces:
			where_str += """ path LIKE "%%%s%%" AND""" % ( self.my_esc_like(piece) )
		if order=="popular":
			where_str = where_str[0:-4] + "  ORDER BY ( requests - kills ) DESC "
		else:
			where_str = where_str[0:-4] + "  ORDER BY path"
		#raise where_str
		self.GetWhere( where_str )
		return

	def SubSearchUsers ( self, query_in, users, order="natural", type="both", recent_days=0, user_logic="OR", query_fields=['path','artist','album','title'], query_logic="OR" ):
		import string
		pieces = re.split(r'[ \t]+', query_in)
		where_str = ""
		for piece in pieces:
			list = []
			for term in query_fields:
				list.append(""" %s LIKE "%%%s%%" """ % ( term, self.my_esc_like(piece) ) )
			if query_logic=="AND":
				where_str += """ ( %s ) AND""" % (" AND ".join(list))
			else:
				where_str += """ ( %s ) AND""" % (" OR ".join(list))
		if recent_days > 0:
			where_str += """ play_history.requestby != 0 AND date > FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d) AND""" % (recent_days*24*60*60)
		where_str = where_str[0:-4] + """ GROUP BY songid"""
		if user_logic == "AND":
			where_str += """, reqby """
		if type == "requests":
			where_str += """ HAVING requests > 0 """
		elif type == "kills":
			where_str += """ HAVING kills > 0 """
		elif type == "netrequests":
			where_str += """ HAVING rank > 0 """
		elif type == "netkills":
			where_str += """ HAVING rank < 0 """
		else:
			where_str += """ HAVING songid """
		if order=="popular":
			where_str += " ORDER BY rank DESC "
		else:
			where_str += " ORDER BY path"
		select = """SELECT user_song_stats.songid,
			SUM(user_song_stats.requests) as requests,
			SUM(user_song_stats.kills) as kills,
			SUM(user_song_stats.requests)-SUM(user_song_stats.kills) as rank,
			songs.path, play_history.date as date, play_history.requestby as reqby
			FROM user_song_stats, songs, play_history
			WHERE user_song_stats.songid = songs.id AND play_history.songid = songs.id
			AND play_history.requestby in (%s) AND %s """ % (users, where_str)
		result = self.do_my_query(select)
		num_users=len(string.split(users,','))
		songs = {}
		for row in result:
			if user_logic == "AND":
				try:
					songs[row[0]] += 1
				except KeyError:
					songs[row[0]] = 1
				if songs[row[0]] == num_users:
					self.list.append(row[0])
			else:
				self.list.append(row[0])
		return



	def SubSearch ( self, query_in, order="natural", type="both", recent_days=0, query_fields=['path','artist','album','title'], query_logic="OR" ):
		where_str = ""
		pieces = re.split(r'[ \t]+', query_in)
		for piece in pieces:
			list = []
			for term in query_fields:
				list.append(""" %s LIKE "%%%s%%" """ % ( term, self.my_esc_like(piece) ) )
			if query_logic=="AND":
				where_str += """ AND ( %s ) """ % (" AND ".join(list))
			else:
				where_str += """ AND ( %s )""" % (" OR ".join(list))
		if type == "requests":
			where_str += " AND requests > 0"
		elif type == "kills":
			where_str += """ AND kills > 0 """
		elif type == "netrequests":
			where_str += """ AND requests > kills """
		elif type == "netkills":
			where_str += """ AND requests < kills """
		if order=="popular":
			where_str += " ORDER BY ( requests - kills ) DESC "
		else:
			where_str += " ORDER BY path"
		if recent_days > 0:
			select = """SELECT songs.id, play_history.date as date FROM songs, play_history
				WHERE play_history.songid = songs.id AND play_history.requestby != 0
				AND date > FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d) %s""" % ((recent_days*24*60*60), where_str)
			result = self.do_my_query(select)
			for row in result:
				self.list.append(row[0])
		else:
			self.GetWhere(where_str[4:])
		return


	def GetRecentPlays ( self, num=3 ):
		self.list = [ ]
		query = """ SELECT songid FROM play_history ORDER BY date DESC LIMIT 1,%d """ % ( num )
		result = self.do_my_query( query )
		for row in result:
			(songid, ) = row
			self.list.append(songid)
		return

	def GetRecentPlaysNew ( self, num=3 ):
		self.list = [ ]
		query = """ SELECT songid,requestby FROM play_history ORDER BY date DESC LIMIT %d """ % ( num )
		result = self.do_my_query( query )
		for row in result:
			(songid, requestby) = row
			self.list.append((songid,requestby))
		return
	def GetTopRank ( self, num ):
		self.list = [ ]
		query = """SELECT id FROM %s ORDER BY requests - kills DESC LIMIT %d""" % ( self.tablename, num )
		result = self.do_my_query( query )
		for row in result:
			(id, ) = row
			self.list.append(id)         
		return                   
	def GetTopRequestsForTime ( self, num=10, days=1):
		"""
		GetTopRankForTime - 
		"""
		self.list=[]
		query="""SELECT songid,count(songid) as number from play_history where requestby != 0 AND date>FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d) GROUP BY songid ORDER BY number DESC LIMIT %d;"""%(days*24*60*60, num)
		result = self.do_my_query( query )
		for row in result:
			(id, num) = row
			self.list.append(id)
		return
