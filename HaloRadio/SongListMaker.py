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

	def SubSearchUsers ( self, query_in, users=None, order="natural", type="both", recent_days=0, user_logic="OR", query_fields=['path','artist','album','title'], query_logic="OR" ):
		import string
		pieces = re.split(r'[ \t]+', query_in)
		where_str = ""
		users_check = ""
		users_check2 = ""
		for piece in pieces:
			list = []
			for term in query_fields:
				list.append(""" %s LIKE "%%%s%%" """ % ( term, self.my_esc_like(piece) ) )
			if query_logic=="AND":
				where_str += """ ( %s ) AND""" % (" AND ".join(list))
			else:
				where_str += """ ( %s ) AND""" % (" OR ".join(list))
		where_str = where_str[0:-4]
		group_str = "GROUP BY songid"
		if user_logic == "AND":
			group_str += """, reqby """
		if order=="popular":
			order_str = " ORDER BY rank DESC "
		else:
			order_str = " ORDER BY path "

		if recent_days > 0:
			if type == "requests" or type == "netrequests" or type == "kills" or type == "netkills":
				group_str += """ HAVING rank > 0 """
			else:
				group_str += """ HAVING songid """
			if type == "kills":
				if users:
					users_check = """ kill_history.killby IN (%s) AND """ % users
				select = """SELECT songs.id as songid, count(songs.id) as rank,
					songs.path as path, kill_history.killby as reqby FROM kill_history, songs
					WHERE songs.id = kill_history.songid AND %s
					kill_history.date > FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d)
					AND %s %s %s""" % (users_check, (recent_days*24*60*60), where_str, group_str, order_str)
			elif type == "requests":
				if users:
					users_check = """ play_history.requestby IN (%s) AND """ % users
				select = """SELECT songs.id as songid, count(songs.id) as rank,
					songs.path as path, play_history.requestby as reqby FROM play_history, songs
					WHERE songs.id = play_history.songid AND %s
					play_history.date > FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d)
					AND %s %s %s""" % (users_check, (recent_days*24*60*60), where_str, group_str, order_str)
			else:
				if order=="popular":
					order_str = " ORDER BY requests DESC, kills ASC "
				else:
					order_str = " ORDER BY path "
				if users:
					users_check = """ play_history.requestby IN (%s) AND """ % users
					users_check2 = """ kill_history.killby IN (%s) AND """ % users
				select = """(SELECT songid, COUNT(songid) AS requests, 0 AS kills FROM play_history
					LEFT JOIN songs ON songs.id = play_history.songid
					WHERE play_history.requestby != 0 AND %s
					play_history.date > FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d) AND %s
					GROUP BY songid) UNION (SELECT songid, 0, COUNT(songid) as kills
					FROM kill_history LEFT JOIN songs ON songs.id = kill_history.songid
					WHERE %s kill_history.date > FROM_UNIXTIME(UNIX_TIMESTAMP(NOW())-%d) AND %s
					GROUP BY songid) %s """ % (users_check, (recent_days*24*60*60),
					where_str, users_check2, (recent_days*24*60*60), where_str, order_str)
				result = self.do_my_query(select)
				songs = {}
				user_cnt = {}
				for row in result:
					try:
						songs[row[0]] += row[1]
						songs[row[0]] -= row[2]
						user_cnt[row[0]] += 1
					except KeyError:
						songs[row[0]] = row[1] - row[2]
						user_cnt[row[0]] = 1
				sortedlist = []
				if order=="popular":
					items=songs.items()
					backitems=[ [v[1],v[0]] for v in items]
					backitems.sort()
					backitems.reverse()
					sortedlist=[ backitems[i][1] for i in range(0,len(backitems))]
				else:
					sortedlist = songs
				num_users = 1
				if users and (user_logic == "AND"):
					num_users=len(string.split(users,','))
				if type == "netrequests":
					for song in sortedlist:
						if (songs[song] > 0) and (user_cnt[song] >= num_users):
							self.list.append(song)
				elif type == "netkills":
					for song in sortedlist:
						if (songs[song] < 0) and (user_cnt[song] >= num_users):
							self.list.append(song)
				else:
					for song in sortedlist:
						if user_cnt[song] >= num_users:
							self.list.append(song)
				return


		else:
			if type == "requests":
				group_str += """ HAVING requests > 0 """
			elif type == "netrequests":
				group_str += """ HAVING rank > 0 """
			elif type == "kills":
				group_str += """ HAVING kills > 0 """
			elif type == "netkills":
				group_str += """ HAVING rank < 0 """
			else:
				group_str += """ HAVING songid """
			if users:
				users_check = """ user_song_stats.userid in (%s) AND """ % users
				select = """SELECT user_song_stats.songid,
					SUM(user_song_stats.requests) as requests,
					SUM(user_song_stats.kills) as kills,
					SUM(user_song_stats.requests)-SUM(user_song_stats.kills) as rank,
					songs.path, user_song_stats.userid as reqby FROM user_song_stats, songs
					WHERE user_song_stats.songid = songs.id AND %s
					%s %s %s""" % (users_check, where_str, group_str, order_str)
			else:
				self.SubSearch(query_in, order=order, type=type, query_fields=query_fields, query_logic=query_logic )
				return
		result = self.do_my_query(select)
		songs = {}
		if user_logic == "AND":
			user_cnt = {}
			num_users=len(string.split(users,','))
			for row in result:
				try:
					songs[row[0]] += row[1]
					songs[row[0]] -= row[2]
					user_cnt[row[0]] += 1
				except KeyError:
					songs[row[0]] = row[1] - row[2]
					user_cnt[row[0]] = 1
			sortedlist = []
			if order=="popular":
				items=songs.items()
				backitems=[ [v[1],v[0]] for v in items]
				backitems.sort()
				backitems.reverse()
				sortedlist=[ backitems[i][1] for i in range(0,len(backitems))]
			else:
				sortedlist = songs
			for song in sortedlist:
				if user_cnt[song] >= num_users:
					self.list.append(song)
		else:
			for row in result:
				self.list.append(row[0])
		return


	def SubSearch ( self, query_in, order="natural", type="both", query_fields=['path','artist','album','title'], query_logic="OR" ):
		where_str = ""
		order_str = ""
		group_str = ""
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
		group_str = " GROUP BY songs.id "
		if order=="popular":
			order_str = " ORDER BY requests DESC "
		else:
			order_str = " ORDER BY path"
		self.GetWhere("""%s %s""" % (where_str[4:], order_str))
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
		query = """SELECT id FROM %s ORDER BY requests DESC LIMIT %d""" % ( self.tablename, num )
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
