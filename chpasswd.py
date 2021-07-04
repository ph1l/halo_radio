#!/usr/bin/python

#
# chpasswd.py - cmd line util for changing ppls passwords.
#
#    Copyright (C) 2004 Philip J Freeman
#
#    This file is part of halo_radio
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


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

