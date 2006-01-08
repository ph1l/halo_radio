#
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
import urllib2, string,re
import HaloRadio

def GetStreamURLList( ):
	urls= HaloRadio.conf['general.status_urls']
	return urls.split(",")

def GetListeners( ):

	# /radio_128,,,3,, - Nine Inch Nails - Rusty Nails 3 #01 - Rusty Nails 3,
	re_listeners = re.compile(r"(%s_[0-9]+,[^,]*,[^,]*,[0-9]+,)"%(HaloRadio.conf['shout.mount']),re.M)

	listeners=int(HaloRadio.conf['general.listener_offset'])

	for url in GetStreamURLList():
		page = "".join(urllib2.urlopen(url).readlines())
		matches = re_listeners.findall(page)
		i=0
		while i < len(matches):
			line_in =  matches[i]
			fields = line_in.split(",")
			try:
				listeners_in = int(fields[3])
			except:
				listeners_in = 0
			listeners = listeners + listeners_in
			i = i + 1

	return listeners
	
def SwapRequests( id1, id2):
   import HaloRadio.Request as Request
   try:
      r1 = Request.Request( id1)
      r2 = Request.Request( id2)
   except:
      return

   if self.userid == 1 and ( r1.requestby != 1 or r2.requestby !=1 ):

      return
   if self.userid > 1 and ( r1.requestby > 1 or r2.requestby > 1):
      import HaloRadio.User as User
      u = User.User(self.userid)
      if not u.admin and ( r1.requestby != self.userid or r2.requestby != self.userid):
         return
         u1 = User.User( r1.requestby )
         u2 = User.User( r2.requestby )
         
   saved_songid = r1.songid
   saved_reqby = r1.requestby

   r1.Update(r2.songid, r2.requestby)
   r2.Update(saved_songid, saved_reqby)

def do_authorize (rights,reqs):
   """
                rights - 
                        a       =       global admin
                        m       =       moderator
                        v       =       verified user
                        U       =       unverified
                        G       =       guest
   """

   import string
   if len(reqs) ==0:
      return 1
   for a in range(0,len(reqs)):
      if string.find(rights,reqs[a]) != -1:
         return 1
   return 0

