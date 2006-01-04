import HaloRadio.TopWeb as TopWeb
import HaloRadio.Request as Request
import HaloRadio.Song as Song
import HaloRadio.Exception as HaloException
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvUG"
	def handler(self, context):
		import HaloRadio.Util as Util
		if self.form.has_key("songids"):
			songids = self.form['songids']
		else:
			self.do_error("must request at least one song")
		list = []
		try :
			for obj in songids:
				list.append(int(obj.value))
		except:
			list.append(int(songids.value))
		num_errors=0
		error_string=""
		for sid in list:
			try:
				r = Request.Request( 0, sid, self.session.userid )
			except HaloException.RequestOverQuota, value:
				num_errors = num_errors + 1
				s = Song.Song(sid)
				error_string = "%s\n[%s failed, over quota]"%(error_string,s.GetDisplayName())
			except HaloException.RequestOverPlayed, value:
				num_errors = num_errors + 1
				s = Song.Song(sid)
				error_string = "%s\n[%s failed, over played]"%(error_string,s.GetDisplayName())


		request_url = "%s?action=RequestQueue" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )
		if num_errors > 0:
			error_string = "%s\n\n\nSome of your requests failed."%(
						error_string )
			self.do_error(error_string)


