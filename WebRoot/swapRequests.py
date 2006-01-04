import HaloRadio.TopWeb as TopWeb
import HaloRadio.Request as Request
import HaloRadio.Exception as HaloException

class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import HaloRadio.Util as Util
		if self.form.has_key("reqid"):
			reqid = int(self.form['reqid'].value)
		if self.form.has_key("swapid"):
			swapid = int(self.form['swapid'].value)
		try:
			r = Request.Request( reqid )
			sr = Request.Request( swapid )
		except HaloException.RequestNotFound:
			self.do_error("trying to swap request that doesn't exist. go back andd reload the page.")
		user = self.session.GetUser()
		if self.do_authorize("a",user.rights):
			r.Swap( swapid )
                elif (self.do_authorize("m",user.rights) and
			( not self.do_authorize("a",r.GetUser().rights) or
			not self.do_authorize("a",sr.GetUser().rights) )
                ):
                                r.Swap( swapid )
		elif (
			user.id == r.requestby and
			user.id == sr.requestby
		):
			r.Swap( swapid )

		if self.form.has_key("viewall") and int(self.form['viewall'].value) != 0:
			request_url = "%s?action=RequestQueue&viewall=1" % ( self.config['general.cgi_url'] )
		else:
			request_url = "%s?action=RequestQueue" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )


