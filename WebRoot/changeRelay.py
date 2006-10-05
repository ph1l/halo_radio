import HaloRadio.TopWeb as TopWeb

class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "a"
	def handler(self, context):
		if self.form.has_key("id"):
			id = int(self.form['id'].value)

		self.configdb.SetConfigItem("current_relay",str(id))
		request_url = "%s?action=Relays" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )


