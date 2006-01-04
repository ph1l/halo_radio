import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "a"
	def handler(self, context):
		import HaloRadio.UserSongStatsListMaker as UserSongStatsListMaker
		import HaloRadio.UserSongStats as UserSongStats
		import HaloRadio.Song as Song
		import HaloRadio.User as User
		import HaloRadio.Exception as Exception

		# Username
		if self.form.has_key("id"):
                        userid = int(self.form['id'].value)
		else:
			userid = self.user.id

		user = User.User(userid)
		context.addGlobal ("userid", userid )
		context.addGlobal ("username", user.name )
		context.addGlobal ("email", user.email )
		context.addGlobal ("rights", user.rights )
		context.addGlobal ("createdate", user.create_time )


