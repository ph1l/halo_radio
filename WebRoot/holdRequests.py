import HaloRadio.TopWeb as TopWeb
import HaloRadio.Request as Request
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import HaloRadio.RequestListMaker as RequestListMaker
		import HaloRadio.Util as Util


		if self.form.has_key("requestids"):
			list = []
			requestids = self.form['requestids']
			try:
				id = int( requestids.value )
				list.append(id)
			except:
				for obj in requestids:
					list.append(int(obj.value))
			if len(list) == 0:
				self.do_error("You didn\'t select anything and you suck at life.")
			for reqid in list:
	                	r = Request.Request( reqid )
	                	user = self.session.GetUser()
	                	if self.do_authorize("a",user.rights):
	                        	r.Hold()
				elif (self.do_authorize("m",user.rights) and
					not self.do_authorize("a",r.GetUser().rights)
				):
					r.Hold()
					
	                	elif ( user.id == r.requestby ):
	                        	r.Hold()

		else:
			rlm = RequestListMaker.RequestListMaker()
			user = self.session.GetUser()
			rlm.GetByUser(user.id)
			if len(rlm.list) == 0:
				self.do_error("You didn\'t select anything and you suck at life.")
			for i in range(0,len(rlm.list)):
				r = Request.Request(rlm.list[i])
				r.Hold()
		
		if self.form.has_key("viewall") and int(self.form['viewall'].value) != 0:
			request_url = "%s?action=RequestQueue&viewall=1" % ( self.config['general.cgi_url'] )
		else:
			request_url = "%s?action=RequestQueue" % ( self.config['general.cgi_url'] )
		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )
