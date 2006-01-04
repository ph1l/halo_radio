#!/usr/bin/python

#
# chpasswd.py - cmd line util for changing ppls passwords.
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

def usage():
	print """
chpasswd.py - halo_radio's command line password util.

usage:
  $ ./chpasswd.py -u <UserName> -p <Password>

		A hermit is a deserter from the army of humanity.

"""


#
#
#

import getopt, sys
import HaloRadio
import HaloRadio.User as User
import HaloRadio.UserListMaker as UserListMaker

try: 
	opts,args = getopt.getopt( sys.argv[1:], "hu:p:", [ "help", "password=", "user="])
except:
	usage()
	sys.exit(2)

user=""
password=""

for o, a in opts:
        if o in ("-h", "--help"):
	                usage()
			sys.exit(0)
	if o in ("-p", "--password"):
			password=a
	if o in ("-u", "--user"):
			user=a
	
if user == "" or password == "":
	usage()
	sys.exit(2)

ulm = UserListMaker.UserListMaker()
ulm.GetByName(user)
u = ulm.GetUser(0)
u.SetPassword(password)

