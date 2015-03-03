from cfficodec import BaseCtoPy


class Env(object):
    """ sophia environment model """

    def __init__(self, sp, sp_path):
        self.sp  = sp
        self.env = self.sp.env()
        self.ctl = self.sp.ctl(self.env)
        rc = self.sp.set( self.ctl, "sophia.path",sp_path)
        self.st_db = "db"
        self.st_dbname = "default_sp_db"
        self.dbs =dict({})

    def open(self):
        rc = self.sp.open( self.env )
        return rc.decode()

    def close(self):
        rc = self.sp.destroy( self.env )
        return rc.decode()



class DB(object):
    """ db abstr model"""              
    def __init__( self, sp_env, dbname ):
        self.env = sp_env
        self.ctl = sp_env.ctl
        self.sp  = sp_env.sp
        codec = BaseCtoPy(self.env.sp)
        self.st_db = "db"
        self.db = None
        self.opened = False
        self.st_dbname = "%s.%s" % (self.st_db,dbname) 
        self.u32 = codec.cast_uint32_t 
        rc = self.sp.set(self.ctl,self.st_db,dbname)

        self.db = self.sp.get(self.ctl,self.st_dbname)
        

    def open(self):
        rc = self.sp.open(self.db)
        if rc.decode() == 0:
           self.opened = True
           return True
        return False

    def close(self):
        if self.opened:
            rc = self.sp.destroy(self.db)
            if rc.decode() == 0:
                self.opened = False
                return True 
        return False

    def _set(self, key, value, len_key, len_value ):
       o = self.sp.object( self.db )
       # check, check, check
       szk = self.sp.ffi.cast("uint32_t",len_key)
       szv = self.sp.ffi.cast("uint32_t",len_value)
       if o.cd != self.sp.ffi.NULL:
           
           rc = self.sp.set(o, "key",key,szk )
           #print "set key",rc.decode()
           #check
           rc = self.sp.set(o, "value",value, szv)
           #print "set value",rc.decode()
           #check
           rc = self.sp.set(self.db , o )
           #check
           #print "sp set db,o",rc.decode()
           rc = self.sp.destroy( o ) # is that needed?
           #check
           return rc


    def set_s_s(self, key, value, ):
        return self._set(key, value, self.u32(len(key)), self.u32(len(value)) )


    def set_u_s(self,key, value ):
        return self._set(key,value,4,len(value) )


    def _get_(self,codec, key):
       o = self.sp.object( self.db )
       sz = self.sp.ffi.new("uint32_t*")
       # how to free this
       if o.cd != self.sp.ffi.NULL:
           szk = self.sp.ffi.cast("uint32_t",len(key))
           rc = self.sp.set( o, "key",key,szk )
           #print "get set key",rc.decode()


           res_o = self.sp.get( self.db, o )

           res_v = self.sp.get(res_o,"value",sz )
           res_v.cd_sz = sz[0] #!
           #check
           #res = res_v.decode()
           #check
           res = codec.decode(res_v.cd,sz[0])
           rc = self.sp.destroy( o )
           rc = self.sp.destroy( res_o )
           #check
           return res




    def _get(self, key,len_key):
       o = self.sp.object( self.db )
       sz = self.sp.ffi.new("uint32_t*")
       # how to free this
       if o.cd != self.sp.ffi.NULL:
           szk = self.sp.ffi.cast("uint32_t",len_key)
           rc = self.sp.set( o, "key",key,szk )
           #print "get set key",rc.decode()


           res_o = self.sp.get( self.db, o )
           
           res_v = self.sp.get(res_o,"value",sz )
           res_v.cd_sz = sz[0] #!
           #check
           res = res_v.decode()
           #check
           rc = self.sp.destroy( o )
           rc = self.sp.destroy( res_o )
           #check
           return res
 

    def get_u(self, key):
        return self._get(key,4)
    def get_s(self,key):
        return self._get(key,len(key) )


