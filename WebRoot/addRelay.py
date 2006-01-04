import HaloRadio.TopWeb as TopWeb

class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "a"
	def handler(self, context):
		import HaloRadio.Relay as Relay

		if self.form.has_key("url"):
			url = self.form['url'].value
		if self.form.has_key("title"):
			title = self.form['title'].value
		if self.form.has_key("comment"):
			comment = self.form['comment'].value

		r = Relay.Relay(0,url,title,comment)

		request_url = "%s?action=Relays" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )


