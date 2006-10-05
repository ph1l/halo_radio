import HaloRadio.TopWeb as TopWeb
import HaloRadio.Request as Request
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "a"
	def handler(self, context):

		for key in ['moderator_enable_access','moderator_wall_enable_access']:
			if self.form.has_key(key):
				self.configdb.SetConfigItem(key, self.form[key].value)

		request_url = "%s?action=Admin" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )


