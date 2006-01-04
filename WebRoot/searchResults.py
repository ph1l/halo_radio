import HaloRadio.TopWeb as TopWeb
import HaloRadio.SongListMaker as SongListMaker
import HaloRadio.UserListMaker as UserListMaker
import HaloRadio.User as User
import string

class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvUG"
	def handler(self, context):
		pageappend = ""
		if self.form.has_key("search"):
			searchstring = self.form['search'].value
		else:
			searchstring = "NOTHINGwillMATCHthis"
		if self.form.has_key("offset"):
			offset = int(self.form['offset'].value)
		else:
			offset = 0

		if self.form.has_key("limit"):
			limit = int(self.form['limit'].value)
		else:
			limit=15

		if self.form.has_key("sort"):
			sort = self.form['sort'].value
			pageappend += "&sort=%s" % sort
		else:
			sort = "popularity"

		if self.form.has_key("type"):
			type_input = self.form['type'].value
			pageappend += "&type=%s" % type_input
		else:
			type_input = "both"

		if self.form.has_key("userlogic"):
			userlogic_input = self.form['userlogic'].value
			pageappend += "&userlogic=%s" % userlogic_input
		else:
			userlogic_input = "OR"

		if self.form.has_key("recent"):
			try:
				recent = int(self.form['days'].value)
                               	pageappend += "&recent=on&days=%d" % recent
			except ValueError:
				self.do_error("""Invalid input into Past Days: "%s" """ % self.form['days'].value)
		else:
			recent = 0

		query_field = []
		if self.form.has_key("query_fields"):
			value = self.form.getvalue("query_fields", "")
			if not isinstance(value, list):
				if(value.find(',')):
					value = string.split(value,",")
				else:
					value = [value]
			for field in value:
				if field == "path":
					query_field.append("path")
				elif field == "artist":
					query_field.append("artist")
				elif field == "album":
					query_field.append("album")
				elif field == "title":
					query_field.append("title")
			pageappend += "&query_fields=" + "&query_fields=%s" % ",".join(query_field)
		else:
			query_field = ['path','artist','album','title']

		if self.form.has_key("querylogic"):
			querylogic_input = self.form['querylogic'].value
			pageappend += "&querylogic=%s" % querylogic_input
		else:
			querylogic_input = "OR"


		slm = SongListMaker.SongListMaker()

		if self.form.has_key("users"):

			users = []
			import re
			ulm = UserListMaker.UserListMaker()
			value = self.form.getvalue("users", "")
			if isinstance(value, list):
				pageappend += "&users="
				pageappend += "&users=".join(value)
				for user in value:
					usr = ulm.GetByName(re.sub("\(.\)$", "", user))
					users.extend(ulm.list)
			else:
				user = ulm.GetByName(re.sub("\(.\)$", "", value))
				users.extend(ulm.list)
				pageappend += "&users=%s" % value
					
			userids = []
			for id in users:
				userids.append(str(id))
			users = ",".join(userids)
			if sort == "popularity":
				slm.SubSearchUsers( searchstring, users, order="popular", type=type_input, recent_days=recent, user_logic=userlogic_input, query_fields=query_field, query_logic=querylogic_input )
			else:
				slm.SubSearchUsers( searchstring, users, type=type_input, recent_days=recent, user_logic=userlogic_input, query_fields=query_field, query_logic=querylogic_input )
		else:
			if sort == "popularity":
				slm.SubSearch( searchstring, order="popular", type=type_input, recent_days=recent, query_fields=query_field, query_logic=querylogic_input )
			#elif sort == "myPopularity":
			#	slm.SubSearchPath( searchstring, order="mypopularity")
			else:
				slm.SubSearch( searchstring, type=type_input, recent_days=recent, query_fields=query_field, query_logic=querylogic_input )
		numres = len(slm.list)
		options = []
		for option in ('filename','popularity'):
			entity = {}
			entity['name']= option
			if option == sort:
				entity['selected']='true'
			options.append(entity)
		context.addGlobal ("options", options)
		context.addGlobal ("numresults", numres)
		context.addGlobal ("searchstr", searchstring)

		slm.Skip(offset)

		if offset+limit > numres:
			numdisp = numres - offset
		else:
			numdisp = limit

		min = offset+1
		max = offset+numdisp
		tot = numres
		resultlist=[]
		for i in range(0, numdisp):
			s = slm.GetSong(i)
			result={}
			result['id'] = s.id
			result['song'] = s.GetDisplayName()
			result['songlen'] = s.GetDisplayLength()
			try:
				result['requests'] = s.GetRequestsFromUsers( users )
				result['kills'] = s.GetKillsFromUsers( users )
			except:
				result['requests'] = s.requests
				result['kills'] = s.kills
			result['songurl'] = "%s?action=songInfo&id=%d"%( self.config['general.cgi_url'], s.id)
			resultlist.append(result)
		context.addGlobal ("resultlist", resultlist)

                i = 0
		pages=[]
                if offset > 0 :
                        numpages = int ( offset / limit )
                        if ( offset % limit > 0 ) :
                                numpages = numpages + 1
                        for j in range(0,numpages):
                                i = i + 1
				page={}

				page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, (i-1)*limit, limit, pageappend)
				page['pagename']=i;
				pages.append(page)
                i = i + 1
                #print """&nbsp;|&nbsp;%(PAGENUM)d""" % { "PAGENUM": i }
		page={}
		page['pagename']=i;
		pages.append(page)

                if max < tot:
                        numpages = int ( ( tot - max ) / limit )
                        if ( ( tot - max ) % limit > 0 ):
                                numpages = numpages + 1
                        for j in range(0,numpages):
                                i = i + 1
                                newoffset = (i-1)*limit
				page={}
				page['pagename']=i
				page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, (i-1)*limit, limit, pageappend)

				pages.append(page)

		context.addGlobal ("pages", pages)
		context.addGlobal ("searchformaction", self.config['general.cgi_url'])
