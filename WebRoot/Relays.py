import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "a"
	def handler(self, context):

		import HaloRadio.RelayListMaker as RelayListMaker
		import HaloRadio.Relay as Relay

		try:
			currid = int(self.configdb.GetConfigItem("current_relay"))
		except:
			currid = 0
			self.configdb.NewConfigItem("current_relay","0")

		rlm = RelayListMaker.RelayListMaker()
		rlm.GetAll()
		relays = []
		entity = {}
		entity['id'] = 0
		entity['url'] = "None"
		entity['title'] = "None"
		if currid == 0:
			entity['selected'] = 1
		entity['delete_url'] = ""
		relays.append(entity)

		for relayid in rlm.list:
			r = Relay.Relay(relayid)
			entity = {}
			entity['id'] = r.id
			entity['url'] = r.url
			entity['title'] = r.GetDisplayName()
			if currid == r.id:
				entity['selected'] = 1
			entity['delete_url'] = "%s?action=deleteRelay&id=%s" % ( self.config['general.cgi_url'],r.id )


			relays.append(entity)
		context.addGlobal ("relays", relays)
		
                context.addGlobal ("formaction", self.config['general.cgi_url'])
