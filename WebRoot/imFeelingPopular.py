import HaloRadio.TopWeb as TopWeb
import HaloRadio.Request as Request
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvUG"
	def handler(self, context):
		import HaloRadio.Util as Util
		if self.form.has_key("search"):
			search = self.form['search'].value
		else:
			search = "GAWDthisISghettoBUTkindaCONSISTANT"
		import HaloRadio.SongListMaker as SongListMaker
		slm = SongListMaker.SongListMaker()
		slm.SubSearchPath( search, order="popular" )

		if len(slm.list) > 0:
			r = Request.Request( 0, slm.list[0], self.session.userid )
		else:
			self.do_error("search (%s), not popular enough..."%
				(search) )

		request_url = "%s?action=RequestQueue" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )


