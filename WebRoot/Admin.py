import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "a"
	def handler(self, context):
		import HaloRadio.PlaylistListMaker as PlaylistListMaker
		import HaloRadio.Playlist as Playlist

		import HaloRadio.Config as Config

		cfg = Config.Config()
		curplid = int(cfg.GetConfigItem("current_list"))
		pllm = PlaylistListMaker.PlaylistListMaker()
		pllm.GetAll()
		playlists = []
		for playlistid in pllm.list:
			pl = Playlist.Playlist(playlistid)
			entity = {}
			entity['id'] = pl.id
			entity['name'] = pl.GetDisplayName()
			if curplid == pl.id:
				entity['selected'] = 1
			playlists.append(entity)
		context.addGlobal ("playlists", playlists)

                context.addGlobal ("formaction", self.config['general.cgi_url'])
