import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvUG"
	def handler(self, context):
		import string
		streams=[]
		clonerates=string.split(self.config['shout.bitrate'],",")
		for br in clonerates:
			entity = {}
			entity['bitrate'] = br
			entity['playlistlink'] = "http://%s:%s%s_%s.m3u" % (
				self.config['shout.host'],
				self.config['shout.port'],
				self.config['shout.mount'],
				br,
				)
			streams.append(entity)
		context.addGlobal ("streams", streams )
