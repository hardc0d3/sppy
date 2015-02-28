'''
_spapi_cffi

Py cffi wrapper Copyright (c) Dobri Stoilov
BSD License
'''

import cffi
from _spapi import SpApi
null=None



class SpApiFFI(SpApi):
    """ sophia api wrapper """



    def __init__( self, cdef, sodll ):
        self.ffi = cffi.FFI() 
        self.f = self.ffi
        self.cdef = cdef
        self.f.cdef( self.cdef )
        self.lib = self.f.dlopen( sodll )
        global null
        null = self.f.NULL
    
    def env(self):
        return self.lib.sp_env()

    def ctl(self, env=null):
        if env != null: 
            return self.lib.sp_ctl( env )
        return null

    def object( self, db=null, cursor=null ):
        #
        #return self.c.sp_object( db or cursor )
        pass
    def open( self, db = null, env = null):
        #print "d: open, db, env:", db,env
        if env != null and db == None:
            return self.lib.sp_open( env )
        if db != null and env == None:
            return self.lib.sp_open( db )

    def destroy( self, res = null):
        if res != null:
            return self.lib.sp_destroy( res )
    
    def error( self, env = null):
        pass
    def set( self, ctl = null, ctlkey = null, ctlval = null, 
             db = null, obj = null,  
             transaction = null,
             field = null, ptr =null, size =null   ):

        if ctl != null and ctlkey != null and ctlval != null:
            return self.lib.sp_set( ctl, ctlkey, ctlval )
  

        return self.f.cast( "int",-1)
 
    def delete(self, db = null, obj = null, transaction = null):
        pass
    def get(self, ctl = null, ctlkey = null, db = null,
            obj = null, transaction = null,
             field  = null, size = null):

        if ctl !=null and ctlkey !=null:
            return self.lib.sp_get(ctl,ctlkey) 

        pass
    # delete snapshot or close db := destroy(res=db)
    def drop(self, snapshot = null, db = null):
        pass
    def cursor(self, ctl = null, db = null, obj = null):
        pass
    def begin(self, env = null):
        pass
    def commit(self, transaction = null):
        pass
    # res := resource should sophia:
    # env, ctl, db, obj, snapshot,
    # transaction, cursor
    def sptype(self, res=null):
        if res != null:
            return self.lib.sp_type(res)
        pass

