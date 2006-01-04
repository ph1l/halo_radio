import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import os
		from_dir= "%s/WebRoot" % (self.config["general.webroot"] )
		files = os.listdir(from_dir)
		stats = []
		for file in files:
			#print file[-4:], file[0:4]
			if file[-4:] == "html" and file[0:4] == "stat":
				name=file[4:-5]
				plug = self.my_import("WebRoot.stat%s"%name)
				#print dir(plug)
				obj = plug.plugin(self.form, self.session)
				if obj.do_authorize(self.user.rights,obj.reqs) == 0:
					continue

				entity = {}
				entity['link'] = "%s?action=stat%s" % ( self.config['general.cgi_url'], name )
				entity['name'] = name
				stats.append(entity)
		context.addGlobal ("stats", stats)

