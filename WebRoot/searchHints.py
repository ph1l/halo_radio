import HaloRadio.TopWeb as TopWeb
import HaloRadio.SongListMaker as SongListMaker
import HaloRadio.UserListMaker as UserListMaker
import HaloRadio.User as User
import HaloRadio.Util as Util
import string

class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvUG"
	def handler(self, context):
		pageappend = ""
		recent = 0
		if self.form.has_key("q"):
			searchstring = self.form['q'].value
		results = Util.GetSearchHints(searchstring)

		hintlist=[]
		for r in results:
			entity={}
			entity['text'] = r
			entity['link'] = "HaloRadio.cgi?action=searchResults&search=%s&sort=popularity"%(r)
			hintlist.append(entity)

		context.addGlobal ("hintlist", hintlist)
