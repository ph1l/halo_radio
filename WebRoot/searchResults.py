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
		recent = 0
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
				slm.SubSearchUsers( searchstring, users=users, order="popular", type=type_input, recent_days=recent, user_logic=userlogic_input, query_fields=query_field, query_logic=querylogic_input )
			else:
				slm.SubSearchUsers( searchstring, users=users, type=type_input, recent_days=recent, user_logic=userlogic_input, query_fields=query_field, query_logic=querylogic_input )
		else:
			if sort == "popularity":
				slm.SubSearchUsers( searchstring, order="popular", type=type_input, recent_days=recent, query_fields=query_field, query_logic=querylogic_input )
			#elif sort == "myPopularity":
			#	slm.SubSearchPath( searchstring, order="mypopularity")
			else:
				slm.SubSearchUsers( searchstring, type=type_input, recent_days=recent, query_fields=query_field, query_logic=querylogic_input )
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
		context.addGlobal ("advsearch", self.config['general.cgi_url'] + "?action=advancedSearch")

		#slm.Skip(offset)

		if offset+limit > numres:
			numdisp = numres - offset
		else:
			numdisp = limit

		min = offset+1
		max = offset+numdisp
		tot = numres
		resultlist=[]
		for i in range(offset, offset + numdisp):
			s = slm.GetSong(i)
			result={}
			result['id'] = s.id
			result['song'] = s.GetDisplayName()
			result['songlen'] = s.GetDisplayLength()
			if self.form.has_key("users") and self.form.has_key("recent"):
				result['requests'] = s.GetRequestsFromUsers( users, recent=recent )
				result['kills'] = s.GetKillsFromUsers( users, recent=recent )
			elif self.form.has_key("users"):
				result['requests'] = s.GetRequestsFromUsers( users )
				result['kills'] = s.GetKillsFromUsers( users )
			elif self.form.has_key("recent"):
				result['requests'] = s.GetNumRecentRequests( days=recent )
				result['kills'] = s.GetNumRecentKills( days=recent )
			else:
				result['requests'] = s.requests
				result['kills'] = s.kills
			result['songurl'] = "%s?action=songInfo&id=%d"%( self.config['general.cgi_url'], s.id)
			resultlist.append(result)
		context.addGlobal ("resultlist", resultlist)

		pages=[]
		pagefootlimit=20                
		subsetmax=pagefootlimit*limit
               	numpages = int ( (tot -1) / limit +1 )

		if offset==0:
			curpage=1
		else :
			curpage=( offset/limit+1 )

                context.addGlobal ("curpage", curpage)
		context.addGlobal ("totpage", numpages)                                                                     
		if ( numpages < pagefootlimit ):
			i=0
			if curpage > 1:
				page={}
				page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, (curpage-2)*limit, limit, pageappend)
				page['pagename']="<<"
				pages.append(page)
			for j in range(0,numpages):
				i = i + 1
                                page={}
				if j==curpage-1:
					page['pagename']=i
					pages.append(page)
				else :
					page={}
					page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, (i-1)*limit, limit, pageappend)
					page['pagename']=i
					pages.append(page)


			if curpage<numpages:
				page={}
				page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, (curpage)*limit, limit, pageappend)
				page['pagename']=">>"
				pages.append(page)

			context.addGlobal ("pages", pages)
			context.addGlobal ("searchformaction", self.config['general.cgi_url'])

		else:
			i=0
			if curpage <= (pagefootlimit / 2):
				if curpage != 1:
					page={}
					page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, (curpage-2)*limit, limit, pageappend)
					page['pagename']="<<"
					pages.append(page)
				for j in range(0,pagefootlimit):
					i = i + 1
					if j==curpage-1:
                                		page={}
						page['pagename']=i
						pages.append(page)
					else :
						page={}
						page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, (i-1)*limit, limit, pageappend)
						page['pagename']=i
						pages.append(page)


				page={}
				page['pagename']=".."
				pages.append(page)
				page={}
				page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, ((tot/limit+1)*limit - limit), limit, pageappend)
				page['pagename']=(tot/limit+1)
				pages.append(page)
				page={}
				page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, (curpage)*limit, limit, pageappend)
				page['pagename']=">>"
				pages.append(page)
				context.addGlobal ("pages", pages)
				context.addGlobal ("searchformaction", self.config['general.cgi_url'])
			else:
				halfpagefootlimit=pagefootlimit/2
				page={}
				page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, (curpage-2)*limit, limit, pageappend)
				page['pagename']="<<"
				pages.append(page)
				page={}
				page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, 0, limit, pageappend)
				page['pagename']=1
				pages.append(page)
				page={}
				page['pagename']=".."
				pages.append(page)
				
				if ( (curpage+halfpagefootlimit) > numpages ):
					lastpage=numpages
				else:	
					lastpage=curpage+halfpagefootlimit
				
				i=curpage-halfpagefootlimit
				for j in range(curpage-halfpagefootlimit,lastpage):
					i = i + 1
					page={}
					if j==curpage-1:
						page['pagename']=i
						pages.append(page)
					else :

						page={}
						page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, (i-1)*limit, limit, pageappend)
						page['pagename']=i
						pages.append(page)

                        	if curpage<(numpages-(pagefootlimit/2)):
					page={}
					page['pagename']=".."
					pages.append(page)
					page={}
					page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, ((tot/limit+1)*limit - limit), limit, pageappend)
					page['pagename']=(tot/limit+1)
					pages.append(page)
                        	if curpage<numpages:
					page={}
					page['pagelink']="%s?action=searchResults&search=%s&offset=%s&limit=%s%s"%( self.config['general.cgi_url'], searchstring, (curpage)*limit, limit, pageappend)
					page['pagename']=">>"
					pages.append(page)
				context.addGlobal ("pages", pages)
				context.addGlobal ("searchformaction", self.config['general.cgi_url'])
