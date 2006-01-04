import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "G"
	def handler(self, context):
		
		context.addGlobal ("formaction", self.config['general.cgi_url'])
		context.addGlobal ("newuserurl", "%s?action=newUser"%(self.config['general.cgi_url']))
		context.addGlobal ("forgotpasswordurl", "%s?action=forgotPassword"%(self.config['general.cgi_url']))
