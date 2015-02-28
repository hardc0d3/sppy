'''
_spapi_cffi

Py cffi wrapper Copyright (c) Dobri Stoilov
BSD License
'''

import cffi
from _spapi import SpApi
null=None

class NTMBS(object):
     def __init__(self,ffi):
         self.ffi = ffi
     def decode( self,nts, sz ):
         return self.ffi.string( self.ffi.cast ("char*",nts ) ) 


class Wrap(object):
    """ cffi & sophia object wrapper """
    def __init__(self, sp, codec, fun, args ):
        #print "args",args
        #print "fun", fun
        self.sp = sp
        self.ret = self.sp.ffi.NULL
        self.ret_sz = 0
        self.codec = codec
        #print self.ret
        if len(args) == 0:
            self.ret = fun() 
        newargs = tuple([ x.ret for x in args ])
        #print "newargs",newargs
        self.ret = fun( *newargs )
        #print "ret",self.ret
        self._ = self.decode

    def decode(self):
        if self.codec is None or self.ret == self.sp.ffi.NULL: 
            return None
        return self.codec.decode ( self.ret, self.ret_sz )




class SpApiFFI(SpApi):
    """ sophia api wrapper """

    def __init__( self, cdef, dl ):
        self.ffi = cffi.FFI() 
        self.f = self.ffi
        self.cdef = cdef
        self.f.cdef( self.cdef )
        self.lib = self.f.dlopen( dl )
        self.null = self.f.NULL
        self.codec_ntmbs = NTMBS(self.ffi) 
    
    def env(self, *args):
                   # sp,  codec,  fun,           args
        return Wrap( self, None, self.lib.sp_env, args)

    def ctl(self, *args ):
        return  Wrap( self,None, self.lib.sp_ctl, args ) 

    def object( self, *args ):
        return Wrap(self,None, self.lib.sp_object , args )

    def open( self, *args):
        return self.lib.sp_open( *args )

    def destroy( self, *args):
        return self.lib.sp_destroy( *args )
    
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
        return Wrap(self,self.codec_ntmbs, self.lib.sp_type, args)


