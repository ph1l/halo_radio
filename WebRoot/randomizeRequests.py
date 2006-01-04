import HaloRadio.TopWeb as TopWeb
import HaloRadio.Request as Request
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import HaloRadio.Util as Util
		if self.form.has_key("requestids"):
			requestids = self.form['requestids']
		else:
			self.do_error("You didn\'t select anything and you suck at life.")
		
		list = []
		try:
			id = int( requestids.value )
			list.append(id)
		except:
			for obj in requestids:
				list.append(int(obj.value))
		user = self.session.GetUser()
		doit=0
		user=self.session.GetUser()
		urights=user.rights
		if urights == "a" or urights == "m":
			doit=1
		else:
			doit=1
			for i in range(0,len(list)):
				r = Request.Request(list[i])
				if r.requestby != user.id:
					doit=0
		if doit:
			import random
			for i in range(0,len(list)*3):
				r = Request.Request(
				  list[random.randrange(0,len(list))]
				)
				r.Swap(
				  list[random.randrange(0,len(list))]
				)


		if self.form.has_key("viewall") and int(self.form['viewall'].value) != 0:
			request_url = "%s?action=RequestQueue&viewall=1" % ( self.config['general.cgi_url'] )
		else:
			request_url = "%s?action=RequestQueue" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )


