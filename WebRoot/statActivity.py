import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvUG"
	def handler(self, context):
		import HaloRadio.Util as Util

		context.addGlobal ("listeners", Util.GetListeners())

		graphlist =[]
		timelist=('daily','weekly','monthly','yearly')
		#timelist=('daily','weekly', 'monthly')

		for time in timelist:
			entity={}
			entity['url']="%s/halostat--activity-%s.png" % (self.config['general.root_url'], time)
			graphlist.append(entity)
		context.addGlobal ("graphs", graphlist)

