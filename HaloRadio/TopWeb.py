import HaloRadio

class TopWeb:
	def __init__(self, form, session):
		self.config = HaloRadio.conf
		self.configdb = HaloRadio.configdb
		self.form = form
		self.session = session
		self.reqs = self.GetReqs()
		self.user = self.session.GetUser()

	def LoadAuth(self):
		if self.do_authorize(self.user.rights, self.reqs) == 0:
			self.do_error("Unauthorized")

	def do_authorize(self,rights,reqs):
		import string
		##print "do_authorize(rights=%s,reqs=%s)"%(rights,reqs)
		if len(reqs) ==0:
			return 1
		for a in range(0,len(reqs)):
			if string.find(rights,reqs[a]) != -1:
				return 1
		return 0

	def do_error(self, errorstr):
		from simpletal import simpleTAL, simpleTALES
		import sys
		context = simpleTALES.Context( )
		templateFile = open ("%s/WebRoot/error.html"%(self.config['general.webroot']) , 'r')
	   	template = simpleTAL.compileHTMLTemplate (templateFile)
	   	templateFile.close()
		context.addGlobal ("error", errorstr)
		template.expand (context, sys.stdout)
		sys.exit()

	def my_import(self, name):
	        mod = __import__(name)
	        components = name.split('.')
	        for comp in components[1:]:
	                mod = getattr(mod, comp)
	        return mod

