import cffi

_cdef = """
void *malloc(size_t size);
void free(void *ptr);
void *calloc(size_t nmemb, size_t size);
void *realloc(void *ptr, size_t size);
void *memcpy(void *dest, const void *src, size_t n);

"""


class EncoderDecoder(object):

    def __init__( self ):
        self.ffi = cffi.FFI()
        self.ffi.cdef (_cdef)
        self.lib = self.ffi.dlopen(None)
        self._TYPE_STR = 99
        self._TYPE_UTF8 = 100 
        self._TYPE_SZ = 1
        self._MAXLEN_TYPE = 1
        self._MAXLEN_STR = 2

   
    def enc_str( self, s, itp ):
        sc="xxxx"+s
        cdata = self.ffi.new("char []",sc)
        ctype = self.ffi.new('uint8_t *',itp)
        clen  = self.ffi.new('uint16_t *',len(s) )
        print cdata
        typebuff =  self.ffi.buffer(ctype,2)        
        lenbuff  =  self.ffi.buffer(clen, 2)
        databuff = self.ffi.buffer(cdata,len(sc))
        databuff[1] = typebuff [0]
        databuff[2] = lenbuff  [0]
        databuff[3] = lenbuff  [1]

        for c in databuff:
            print ('enc',c)
        return cdata

    def dec_str( self, cdata ):
        buff = self.ffi.buffer ( cdata, 4 )
        ctype = self.ffi.new('uint8_t*',0 )
        clen  = self.ffi.new('uint16_t*',2 )
        lenbuff = self.ffi.buffer ( clen, 2 )
        typebuff = self.ffi.buffer ( ctype, 1 )
        typebuff[0] = buff [1]
        lenbuff[0] = buff [2]
        lenbuff[1] = buff [3]         
        buff = self.ffi.buffer ( cdata, clen[0]+4 ) 
        for c in buff:
            print ('dec',c)
 
        return ctype[0],clen[0],buff[4:]



    def enc_utf8( self, u8 ):
        st = u8.encode('utf-8')
        print ("encu8",u8,st,len(st))
        #print "St",st
        return self.enc_str(st,self._TYPE_UTF8)



    def dec_utf8( self, cd):
        r = self.dec_str( cd )
        return r


