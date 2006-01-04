import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import HaloRadio.WallListMaker as WallListMaker
		import HaloRadio.Wall as Wall
		import HaloRadio.Exception as HaloException

		wlm = WallListMaker.WallListMaker()
		wlm.GetRecent(75)
		walls = []
		for wallid in wlm.list:
			wall = Wall.Wall(wallid)
			line = wall.line
			user = wall.GetUser()
			entity = {}
			if line[0:4] == "/me ":
				entity['line'] = "%s %s"%(user.GetDisplayName(),line[4:])
				entity['username'] = ""
			else:
				entity['line'] = line
				entity['username'] = user.GetDisplayName()
			entity['userlink'] = "%s?action=userInfo&id=%s" % (self.config['general.cgi_url'], user.id )
			entity['date'] = wall.date
			walls.append(entity)
		context.addGlobal ("walllist", walls)

		context.addGlobal ("formaction", self.config['general.cgi_url'])
