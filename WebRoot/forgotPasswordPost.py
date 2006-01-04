import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "G"
	def handler(self, context):
		import string
		if self.form.has_key("email"):
			email = self.form['email'].value
		if string.find(email,"@") == -1:
			self.do_error ("gimme a real email. i need it to verify your existence. :-P")
		if len(email) < 3:
			self.do_error ("gimme a real email. i need it to verify your existence. :-P")

		import HaloRadio.UserListMaker as UserListMaker

		ulm = UserListMaker.UserListMaker()

		ulm.GetByEmail(email)

		if  len(ulm.list) < 1:
			self.do_error("no user found for that email")
		if  len(ulm.list) > 1:
			self.do_error("too many users found for that email")
		u = ulm.GetUser(0)

		hash = u.GetNewHash()	

		import sendmail

		emailstr = """From: %(from)s
To: %(to)s
Bcc: %(bcc)s
Subject: %(site_name)s password request

%(user)s - 

someone requested a forgotten password...

  click here : 
%(siteurl)s/?action=verify&user=%(user)s&hash=%(code)s



"""% {
	"from": "halo_radio@server",
	"to": email,
	"site_name": "halo_radio",
	"bcc": "phil@kremlor.net",
	"code": hash,
	"user": u.name,
	"siteurl": self.config["general.cgi_url"]
}

		sendmail.sendmail( "halo_radio@server", [ email, "phil@kremlor.net" ], emailstr )
