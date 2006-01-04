import HaloRadio.TopTable as TopTable
            
class Session(TopTable.TopTable):
   authenticated = 0
   """      
   - Session - CLASS  
   """      
   def __init__( self, inid, user="", passwd="" ):
      self.tablename = "session"
      newid=""   
      if inid == None:
         import time,random,string
         newid = "%s-" % time.strftime( "%Y%m%d%H%M%S" )
         for a in range(0,127):
            newid += random.choice(string.ascii_letters + string.digits)          
         id = self.do_my_insert( """INSERT INTO %s SET id=\"%s\", userid=%d, create_time=NOW(), active_time=NOW();""" %
            ( self.tablename, newid, 1) )
      else:      
         newid = inid
            
      """load up the info for the provided id"""
      rows = self.do_my_query( """SELECT userid, host FROM %s WHERE id="%s";""" % ( self.tablename, newid ) )
      try:       
         (self.userid, self.host) = rows[0]
      except IndexError:
         raise "unable to load data for request(%s)" % newid
      self.id = newid
      return     
   def GetUser( self ):
      import HaloRadio.User as User
      user = User.User(self.userid)
      return user

   def SetUser( self, user ):
      self.do_my_do( """UPDATE %s SET userid=%d,active_time=NOW() WHERE id="%s";""" %       
         ( self.tablename, user.id, self.id) )
            
      self.userid=user.id

   def Authenticate( self, user, password ):
      import HaloRadio.User as User
            
      authenticated=1
      try:       
      	m=User.User(-1,user,password)
      except:    
         authenticated=0

      if authenticated:
         self.do_my_do( """UPDATE %s SET userid=%d,active_time=NOW() WHERE id="%s";""" %      
            ( self.tablename, m.id, self.id) )
         self.userid=m.id
   def UpdateActivity( self ):
       self.do_my_do( """UPDATE %s SET active_time=NOW() WHERE id="%s";""" %
         ( self.tablename, self.id ))
   def GetActivity( self ):
      rows=self.do_my_query( """ SELECT active_time FROM %s WHERE id="%s";""" %
         ( self.tablename, self.id) )
      row=rows[0]
      activetime = row[0]
      return activetime
   def SetHost( self, host ):
      self.do_my_do( """UPDATE %s SET host="%s" WHERE id="%s";""" %
         ( self.tablename, host,  self.id ))
      self.host = host
