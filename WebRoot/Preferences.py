import HaloRadio.TopWeb as TopWeb
import HaloRadio.StyleListMaker as StyleListMaker
import HaloRadio.Style as Style
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
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
		if (self.do_authorize(self.user.rights, "a")):
			is_admin=1
			readonly=0
		else:
			is_admin=0
			readonly=1
		context.addGlobal ("is_admin", is_admin)
		context.addGlobal ("readonly", readonly)
		context.addGlobal ("userid", userid )
		context.addGlobal ("username", user.name )
		context.addGlobal ("email", user.email )
		context.addGlobal ("rights", user.rights )
		context.addGlobal ("createdate", user.create_time )
		slm = StyleListMaker.StyleListMaker()
		slm.GetAll()
		styles = []
		for styleid in slm.list:
			style = Style.Style(styleid)
			entity = {}
			entity['style'] = style.GetName()
			entity['id'] = style.GetId()
			styles.append(entity)
		context.addGlobal ("styles", styles )
