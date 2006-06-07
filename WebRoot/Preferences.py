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
			is_user=0
			canmod_user=1
			ro_user=0
			canmod_rights=1
			ro_rights=0
			canmod_email=1
			ro_email=0
			canmod_passwd=1
			ro_passwd=0
		elif (self.do_authorize(self.user.rights, "m")):
			is_user=0
			canmod_user=0
			ro_user=1
			canmod_rights=0
			ro_rights=1
			canmod_email=1
			ro_email=0
			canmod_passwd=1
			ro_passwd=0
		else:
			is_user=1
			canmod_user=0
			ro_user=1
			canmod_rights=0
			ro_rights=1
			canmod_email=0
			ro_email=1
			canmod_passwd=1
			ro_passwd=0

		context.addGlobal ("is_user", is_user)
		context.addGlobal ("canmod_user", canmod_user )
		context.addGlobal ("ro_user", ro_user)
		context.addGlobal ("canmod_rights", canmod_rights)
		context.addGlobal ("ro_rights", ro_rights)
		context.addGlobal ("canmod_email", canmod_email)
		context.addGlobal ("ro_email", ro_email)
		context.addGlobal ("canmod_passwd", canmod_passwd)
		context.addGlobal ("ro_passwd", ro_passwd)
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
