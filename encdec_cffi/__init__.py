

class EncoderDecoder(object):

    def __init__( self, ffi ):
        self.ffi = ffi

    def enc_str( self, s ):
        return self.ffi.new( 'char []',s )

    def dec_str( self, cs ):
        return self.ffi.string( self, cs )

    def enc_utf8( self, u8 ):
        return self.ffi.new ( 'char []', u8.encode('utf-8') )

    def dec_utf8( self, cu8 ):
        return self.ffi.string ( cu8 ).decode('utf-8')

    def enc_num( self,typestr, num):
        return self.ffi.cast(typestr,num)


    def enc_unum( self, typestr ,num ):
        if ( num >= 0 ):
             return self.ffi.cast("unsigned %s" % typestr , num)
        else:
             raise Exception ("must be >=0 ")

    def dec_int( self, cnum ):
             return int( cnum )
  
    def dec_long( self,cnum):
             return int ( cnum )

    def dec_float( self,cnum):
             return float( cnum ) 



   
