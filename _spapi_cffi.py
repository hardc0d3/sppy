'''
_spapi_cffi
python cffi based wrapper for SophiaDB, sphia.org

Copyright (c) Dobri Stoilov hardc0d3
BSD License
'''

import sys
sys.path.append('../cfficodecs')


from numbers import Number
import cffi
import _spapi_cdef
from _spapi import SpApi
from cfficodec import BaseCtoPy
null=None

class NTMBS(object):
     def __init__(self,ffi):
         self.ffi = ffi

     def decode( self,nts, sz ):
         return self.ffi.string( self.ffi.cast ("char*",nts ) ) 

     def encode( self, s):
         return self.ffi.new("char[]",s)

class CharLen(object):
     def __init__(self,ffi):
         self.ffi = ffi

     def decode( self,nts, sz ):
         return self.ffi.buffer( self.ffi.cast ("char*",nts ),sz )[:]



class CastIntCodec(object):
     def __init__(self,ffi):
         self.ffi = ffi

     def decode( self,ci, sz ):
         return int(ci) 

     def encode( self, i):
         return self.ffi.cast("int",i)



class Wrap(object):
    """ cffi & sophia object wrapper """
    def __init__(self, sp, codec, fun, args ):
        self.sp = sp
        self.cd  = self.sp.ffi.NULL
        self.cd_sz = 0
        self.codec = codec
        self._ = self.decode
        # to support ordering
        self.cdargs = [null]*len(args)
        self.in_codec = BaseCtoPy(self.sp)


        for argt in enumerate(args):
            if isinstance(argt[1],Wrap):
                self.cdargs[argt[0]]=argt[1].cd
            if isinstance(argt[1],sp.ffi.CData):
                self.cdargs[argt[0]]=argt[1]
            # not needed now
            if isinstance(argt[1], Number):
                #to doget param input codec
                self.cdargs[argt[0]]=self.in_codec.new_uint32_t(argt[1])
            
            if isinstance(argt[1], str ):
                    self.cdargs[ argt[0]] = ( NTMBS( sp.ffi ).encode( argt[1] ) ) 
                    pass
        if len(self.cdargs) == 0:
            self.cd = fun()
        else:
            self.cd = fun( *self.cdargs)
        

    def decode(self):
        if self.codec is None or self.cd == self.sp.ffi.NULL: 
            return None
        return self.codec.decode ( self.cd, self.cd_sz )




class SpApiFFI(SpApi):
    """ sophia api wrapper """

    def __init__( self, dl ):
        self.ffi = cffi.FFI() 
        self.f = self.ffi
        self.cdef = _spapi_cdef.cdef 
        self.f.cdef( self.cdef )
        self.lib = self.f.dlopen( dl )
        self.null = self.f.NULL
        self.codec_ntmbs = NTMBS(self.ffi) 
        self.codec_castint = CastIntCodec(self.ffi)
        self.codec_charlen = CharLen(self.ffi) 


    # codec is for returned value.decode()
    def env(self, *args):
                   # sp,  codec,  fun,           args
        return Wrap( self, None, self.lib.sp_env, args)

    def ctl(self, *args ):
        return  Wrap( self,None, self.lib.sp_ctl, args ) 

    def object( self, *args ):
        return Wrap(self,None, self.lib.sp_object , args )

    def open( self, *args):
       #            sp    codec              fun                 args
       return Wrap(self, self.codec_castint, self.lib.sp_open,   args )

    def destroy( self, *args):
       #            sp    codec               fun                  args
        return Wrap(self, self.codec_castint, self.lib.sp_destroy, args )
    
    def error( self, *args):
        return Wrap(self,  self.codec_castint, self.lib.sp_error, args )

    def set ( self, *args ):
        #            sp    codec    fun             args
        return Wrap(self, self.codec_castint , self.lib.sp_set ,args )
 
    def delete(self, *args):
        return Wrap(self, self.codec_castint , self.lib.sp_delete ,args )

    def get( self, *args ):
        # variable arg semantics
        if len(args) == 3 and isinstance(args[1],str):
            # here return data, datasz
            # should make any difference
            #uint32_t size;
            #sp_get(object, "field", &size)
            return Wrap( self, self.codec_charlen, self.lib.sp_get, args )
        else:
            return Wrap( self, None, self.lib.sp_get, args ) 
 
    def drop(self, *args):
        return Wrap(self, self.codec_castint , self.lib.sp_drop ,args )
    
    def cursor(self, *args):
        return Wrap(self, None , self.lib.sp_cursor ,args )
    
    def begin(self, *args):
        return Wrap(self, None , self.lib.sp_begin ,args )
 
    def commit(self, *args):
        return Wrap(self, self.codec_castint , self.lib.sp_commit ,args ) 

    def type( self, *args):
        return Wrap(self,self.codec_ntmbs, self.lib.sp_type, args)


