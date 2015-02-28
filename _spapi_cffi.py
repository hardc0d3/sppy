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

    def __init__( self, cdef, dl ):
        self.ffi = cffi.FFI() 
        self.f = self.ffi
        self.cdef = cdef
        self.f.cdef( self.cdef )
        self.lib = self.f.dlopen( dl )
        self.null = self.f.NULL
    
    def env(self):
        return self.lib.sp_env()

    def ctl(self, *args ):
        return self.lib.sp_ctl( *args )

    def object( self, *args ):
        return self.lib.sp_object ( *args )

    def open( self, *args):
        return self.lib.sp_open( *args )

    def destroy( self, *args):
        return self.lib.sp_destroy( res )
    
    def error( self, *args):
        return self.lib.sp_error( *args) 

    def set ( self, *args ):
        return self.lib.sp_set( *args )
 
    def delete(self, *args):
        return self.lib.sp_delete( *args) 

    def get( self, *args ):
        return self.lib.sp_get( *args )
 
    def drop(self, *args):
        return self.lib.sp_drop( *args)
    
    def cursor(self, *args):
        return self.lib.sp_cursor( *args)
 
    def begin(self, *args):
        return self.lib.sp_begin( *args)
 
    def commit(self, *args):
        return self.lib.sp_commit( *args)

    def type( self, *args):
        return self.lib.sp_type( *args)


