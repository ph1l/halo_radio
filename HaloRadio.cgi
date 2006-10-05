#!/usr/bin/python
#
#    Copyright (C) 2004 Philip J Freeman
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
#

import HaloRadio
import HaloRadio.Session as Session
from HaloRadio.Util import do_authorize
from simpletal import simpleTAL, simpleTALES

# from simpletalutils import HTMLStructureCleaner

import os, cgi, string, sys, StringIO
import cgitb; cgitb.enable()

#logfile = open("/tmp/.newhaloradio.log","w+")
#
#def log( text ):
#	logfile.write( "%s\n" % ( text ) )
#
#log( "startup")
#log( repr(os.environ) )

####
#
# Auth
#

def get_session():
	import Cookie
	if os.environ.has_key('HTTP_COOKIE'):
		C=Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
	else:
		C=Cookie.SimpleCookie()
	if C.has_key('SessionID'):
		try:
			s=Session.Session(C['SessionID'].value)
			s.UpdateActivity()
		except:
			s=Session.Session(None)
			C['SessionID']=s.id
			print C.output()

	else:
		s=Session.Session(None)
		C['SessionID']=s.id
		print C.output()
	env = os.environ

	if env.has_key('REMOTE_HOST'):
		s.SetHost(env['REMOTE_HOST'])
	elif env.has_key('REMOTE_ADDR'):
		s.SetHost(env['REMOTE_ADDR'])
	return s
		
	
def do_template(action, session):
        # Create the context that is used by the template
        context = simpleTALES.Context( )
	fortunestr = ""
	if HaloRadio.conf["general.do_fortune"] == "1":
		f = os.popen("/usr/games/fortune -s")
		fortunestr = f.read()
		f.close()

        context.addGlobal ("qotd", fortunestr)
        context.addGlobal ("menu", get_menuitems(session))
                
        templateFile = open ("%s/WebRoot/%s.html" % (HaloRadio.conf["general.webroot"],action), 'r')      
        template = simpleTAL.compileHTMLTemplate (templateFile )
        templateFile.close()
        return (context, template)

def get_menuitems(session):
	from_dir= "%s/WebRoot" % (HaloRadio.conf["general.webroot"] )
	files = os.listdir(from_dir)
	menuitems = []
	for file in files:
		if file[-4:] == "html" and file[0] in string.uppercase:
			action = file[0:-5]
			if os.access("%s/WebRoot/%s.py" % (HaloRadio.conf["general.webroot"], action), os.F_OK):
				plugin = my_import("WebRoot.%s"%action)
				object = plugin.plugin(form, session)
				u = User.User(session.userid)
				try:
					reqs = object.GetReqs()
				except AttributeError:
					reqs = ""
				if do_authorize(u.rights,reqs):
					menuitems.append({"name": file[0:-5], "link": "%s?action=%s" % (HaloRadio.conf["general.cgi_url"],file[0:-5])})
				else:
					continue
			else:
				menuitems.append({"name": file[0:-5], "link": "%s?action=%s" % (HaloRadio.conf["general.cgi_url"],file[0:-5])})

	#menuitems=[ {"name": "Welcome", "link": "NewHaloRadio.cgi?action=Welcome"}, ]
	return menuitems

def my_import(name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
                mod = getattr(mod, comp)
        return mod



import HaloRadio.User as User

form = cgi.FieldStorage()
session = get_session()
print "Content-type: text/html\n"
u = User.User(session.userid)


if form.has_key("action"):
	
	action = form['action'].value
else:
	action = 'Welcome'

if not int(HaloRadio.conf["general.guest_access"]) and session.userid == 1 and action != "login" and action != "newUser" and action != "newUserPost" and action != "verify" and action != "forgotPassword" and action != "forgotPasswordPost":
	action="Login"

	
if not ( os.access("%s/WebRoot/%s.html" % (HaloRadio.conf["general.webroot"], action), os.F_OK) or os.access("%s/WebRoot/%s.py" % (HaloRadio.conf["general.webroot"], action), os.F_OK) ):
	(context, template) = do_template('error', session )
	context.addGlobal ("error", "Invalid Action Specified")
	context.addGlobal ("style", u.GetStyle())
	template.expand (context, sys.stdout)
	sys.exit()

if not u.GetAccess():
	rights = u.GetDisplayRights()
	if 'guest' not in rights.split(", "):
		(context, template) = do_template('error', session )
		context.addGlobal ("error", "User Disabled")
		context.addGlobal ("style", u.GetStyle())
		template.expand (context, sys.stdout)
		sys.exit()

# do header here ( automaticly generated menu :- )
(context, template) = do_template(action, session)

context.addGlobal ("style", u.GetStyle())
if os.access("%s/WebRoot/%s.py" % (HaloRadio.conf["general.webroot"], action), os.F_OK):
	plugin = my_import("WebRoot.%s"%action)
	object = plugin.plugin(form, session)
	object.LoadAuth()
	object.handler(context)
	
template.expand (context, sys.stdout)

# do footer here


