import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
		if self.config['general.guest_has_signup']=="1":
			return "G"
		else:
			return "z"
	def handler(self, context):
		import string
		if self.form.has_key("user"):
			user = self.form['user'].value
		if self.form.has_key("email"):
			email = self.form['email'].value

		if len(user) < 3 or len(user) > 12:
			self.do_error("username must be greater than 2 and less than 13 characters.")
		if string.find(email,"@") == -1:
			self.do_error ("gimme a real email. i need it to verify your existence. :-P")
		if len(email) < 3:
			self.do_error ("gimme a real email. i need it to verify your existence. :-P")

		import HaloRadio.User as User

		try:
			u = User.User(0,user,'blahblahblah',email)
		except:
			self.do_error("user exists.")
		
		hash = u.GetNewHash()	

		import sendmail

		emailstr = """From: %(from)s
To: %(to)s
Bcc: %(bcc)s
Subject: %(site_name)s email verification

%(to)s - 

  your email address was used to request an account for halo_radio. you've
chosen the name of %(user)s, which is in bad taste, but we'll let it slide
this time.

 click here : 
%(siteurl)s/?action=verify&user=%(user)s&hash=%(code)s


 or, your authorization code is:
%(code)s
 ( to manually enter on the page )


---- end transmission.
"""% {
	"from": "halo_radio@%s"%(self.config["general.hostname"]),
	"to": email,
	"site_name": self.config["general.site_name"],
	"bcc": self.config["general.admin_email"],
	"code": hash,
	"user": u.name,
	"siteurl": self.config["general.cgi_url"]
}

		sendmail.sendmail( "halo_radio@%s"%(self.config["general.hostname"]), [ email, self.config["general.admin_email"] ], emailstr )


		context.addGlobal ("formaction", self.config['general.cgi_url'])
		context.addGlobal ("user",u.name)
