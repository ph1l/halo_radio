import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
		if self.config['general.guest_has_request'] == "1":
                	return "amvUG"
		else:
			return "amv"
	def handler(self, context):
		context.addGlobal ("formaction", self.config['general.cgi_url'])
		context.addGlobal ("advsearch", self.config['general.cgi_url'] + "?action=advancedSearch")

