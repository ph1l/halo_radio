import HaloRadio.TopWeb as TopWeb
import HaloRadio.PlayHistListMaker as PlayHistListMaker
import HaloRadio.RequestListMaker as RequestListMaker
import HaloRadio.SessionListMaker as SessionListMaker
import HaloRadio.Config as Config
import HaloRadio.Exception as Exception
import HaloRadio.User as User
class plugin(TopWeb.TopWeb):
	def GetReqs(self):
		return "amvUG"

	def handler(self, context):

		context.addGlobal ("action", "playHistory")
                if self.form.has_key("numlines"):
                        numlines = int(self.form['numlines'].value)
                else:
                        numlines = 25

		context.addGlobal ("numlines", numlines )

                if self.form.has_key("i"):
                        i = int(self.form['i'].value)
                else:
                        i = 0
		i = i+1

		histlen=numlines
		phlm = PlayHistListMaker.PlayHistListMaker()
		phlm.GetRecentPlays(histlen)

		prevsngs = []


		for i in range(0,histlen):
			try:
				ph = phlm.GetPlayHist(i)
			except:
				continue
			if ph.requestby !=0:
				u = User.User(ph.requestby)
				curreqby = u.GetDisplayName()
			else:
				curreqby = ""

			try:
				cur_song = ph.GetSong()
			except Exception.SongNotFound:
				continue
			listitem = {}
			listitem['sngurl']="%s?action=songInfo&id=%d"%(
				self.config['general.cgi_url'], cur_song.id )
			listitem['sng']=cur_song.GetDisplayName()
			listitem['reqby']=curreqby
			listitem['date']=ph.date
			prevsngs.append(listitem)
		context.addGlobal ("prevsngs", prevsngs)
