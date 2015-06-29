'''
python cffi based wrapper for SophiaDB, sphia.org
'''

import cffi
null=None


class NTMBS(object):
     """ null terminated byte string, ...,  may be is too dangerous """
     def __init__(self,ffi):
         self.ffi = ffi

     def decode( self,nts, sz ):
         return self.ffi.string( self.ffi.cast ("char*",nts ) ) 

     def encode( self, s):
         return self.ffi.new("char[]",s)

class CharLen(object):
     """ char* codec """
     def __init__(self,ffi):
         self.ffi = ffi

     def decode( self,nts, sz ):
         return self.ffi.buffer( self.ffi.cast ("char*",nts ),sz )[:]
  
     def decode_prefix(self, nts, sz, prefix ):
         buf = self.ffi.buffer( self.ffi.cast ("char*",nts ),sz )
         lprefix = len(prefix)
         if lprefix > sz:
             lprefix = sz 
         for i in xrange( lprefix ):
             if buf[i] != prefix[i]:
                 raise StopIteration
         return buf[:] 

class CastIntCodec(object):
     """ cdata integer cffi codec"""
     def __init__(self,ffi):
         self.ffi = ffi

     def decode( self,ci, sz ):
         return int(ci) 

     def encode( self, i):
         return self.ffi.cast("int",i)


class Wrap(object):
    """ wraps sophia dl api and cffi cdata object """
    def __init__(self, sp, codec,  fun, args ):
        self.sp = sp
        # cffi cdata sorage
        self.cd  = self.sp.ffi.NULL
        # and it's size
        self.cd_sz = 0
        self.codec = codec
        # decode alias
        self._ = self.decode
        # to support ordering of args
        self.cdargs = [null]*len(args)
        # todo: handling of arguments should be configurable 
        for argt in enumerate(args):
            if isinstance(argt[1],Wrap):
                self.cdargs[argt[0]]=argt[1].cd
            if isinstance(argt[1],sp.ffi.CData):
                self.cdargs[argt[0]]=argt[1]
            if isinstance(argt[1], str ):
                    self.cdargs[ argt[0]] = ( NTMBS( sp.ffi ).encode( argt[1] ) )
        if len(self.cdargs) == 0:
            self.cd = fun()
        else:
            self.cd = fun( *self.cdargs)
        
    def decode(self,sz):
        """decode to python"""
        if self.codec is None or self.cd == self.sp.ffi.NULL: 
            return None
        return self.codec.decode ( self.cd, sz )

    def prefix(self,sz,prefix):
        """decode prefix"""
        if self.codec is None or self.cd == self.sp.ffi.NULL:
           return None
        return self.codec.decode_prefix ( self.cd, sz, prefix)


class SophiaCmpApi(object):
    """ sophia database custom comparsion api wrap with cffi 
        init with dl_name,cdef str, platform bits 32 or 64 and function name"
        then use self.compare_function to set in sophia control interface,
        currently compare_args are not used ( NULL pointer passed )
        sp.set( ctl, "db.%s.index.cmp"%dbname,  this.compare_func, this.compare_args)
    """

    def __init__( self, dl, cdef, platform_bits, func_name ):
        """ dl file name, cdef string, platform_bits: int 32 or 64, func_name string """
        self.platform_bits = platform_bits
        self.ffi = cffi.FFI()
        self.f = self.ffi
        self.cdef = cdef
        self.f.cdef( self.cdef )
        self.lib = self.f.dlopen( dl )
        self.null = self.f.NULL
        self.func_name = func_name

        self.compare_func = self.f.new("char[%d]"%self.platform_bits)
        self.func_cffi_code = getattr(self.lib,self.func_name)
        self.compare_args = self.null
        rc = self.lib.print_pointer( self.compare_func, self.ffi.cast("size_t",self.platform_bits) , self.func_cffi_code)
        if rc <0:
            raise Exception, e("error printing pointer with function code")
        elif rc == 0:
            raise Exception, e("error printing pointer, zero bytes printed, pointer may be NULL")



class SophiaApi(object):
    """ sophia database api v1.2.2 wrapper based on cffi """

    def __init__( self, dl, cdef ):
        self.ffi = cffi.FFI() 
        self.f = self.ffi
        self.cdef = cdef 
        self.f.cdef( self.cdef )
        self.lib = self.f.dlopen( dl )
        self.null = self.f.NULL
        self.codec_ntmbs = NTMBS(self.ffi) 
        self.codec_castint = CastIntCodec(self.ffi)
        self.codec_charlen = CharLen(self.ffi) 


    # codec is for returned value.decode()
    def env(self, *args):
        return Wrap( self, None, self.lib.sp_env, args)

    def ctl(self, *args ):
        return  Wrap( self,None, self.lib.sp_ctl, args ) 

    def object( self, *args ):
        return Wrap(self,None, self.lib.sp_object , args )

    def open( self, *args):
       return Wrap(self, self.codec_castint, self.lib.sp_open,   args )

    def destroy( self, *args):
        return Wrap(self, self.codec_castint, self.lib.sp_destroy, args )
    
    def error( self, *args):
        return Wrap(self,  self.codec_castint, self.lib.sp_error, args )

    def set ( self, *args ):
        return Wrap(self, self.codec_castint , self.lib.sp_set ,args )
 
    def delete(self, *args):
        return Wrap(self, self.codec_castint , self.lib.sp_delete ,args )

    def get( self, *args ):
        # variable arg semantics
        if len(args) == 3 and isinstance(args[1],str):
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
#v1.2.2
    def async(self, *args):
        return Wrap(self, None , self.lib.sp_async ,args )

