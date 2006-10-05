import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "a"
	def handler(self, context):
		import HaloRadio.PlaylistListMaker as PlaylistListMaker
		import HaloRadio.Playlist as Playlist

		curplid = int(self.configdb.GetConfigItem("current_list"))
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

		config_list = []
		for config_option in ['moderator_enable_access','moderator_wall_enable_access']:
			config_item = {}
			config_item['name'] = config_option
			config_item['data'] = self.configdb.GetConfigItem(config_option)
			config_list.append(config_item)
		context.addGlobal ("config_list", config_list)
