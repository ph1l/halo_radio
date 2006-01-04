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
		if Util.do_authorize(user.rights, "am"):
			users = {}
			users_order = []
			newlist = []

			# build the dictionary of requests and a parallel array of order
			for i in range(0,len(list)):
				r = Request.Request(list[i])
				if users.has_key(r.requestby):
					users[r.requestby].append(list[i])
				else:
					users[r.requestby]=[]
					users[r.requestby].append(list[i])
					users_order.append(r.requestby)


			# build the order that the songs should be in
			j = 0
			for i in range(0,len(list)):
				if j >= len(users_order):
					j = 0
				while len(users[users_order[j]]) == 0:
					del users[users_order[j]]
					if j == 0:
						users_order=users_order[1:]
					else:
						users_order_new=users_order[:j]
						users_order_new.extend(users_order[j+1:])
						users_order=users_order_new
					if j >= len(users_order):
						j = 0
				newlist.append(users[users_order[j]][0])
				users[users_order[j]]=users[users_order[j]][1:]
				j=j+1

			# build parallel arrays of the new ordered songs and requestby
			request_by = []
			song_id = []
			held = []
			for element in newlist:
				r=Request.Request(element)
				request_by.append(r.requestby)
				song_id.append(r.songid)
				held.append(r.hold)

			# lock the table and update them all
			l=Request.Request(list[0])
			try:
				l.Lock()
				for song in list:
					r=Request.Request(song)
					r.Update(song_id[0],request_by[0],held[0])
					song_id=song_id[1:]
					request_by=request_by[1:]
					held=held[1:]
				l.Unlock()
			except:
				l.Unlock()
		else:
			self.do_error("Unauthorized")

		if self.form.has_key("viewall") and int(self.form['viewall'].value) != 0:
			request_url = "%s?action=RequestQueue&viewall=1" % ( self.config['general.cgi_url'] )
		else:
			request_url = "%s?action=RequestQueue" % ( self.config['general.cgi_url'] )
		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )


