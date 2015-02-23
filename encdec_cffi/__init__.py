import cffi

_cdef = """
void *malloc(size_t size);
void free(void *ptr);
void *calloc(size_t nmemb, size_t size);
void *realloc(void *ptr, size_t size);
void *memcpy(void *dest, const void *src, size_t n);

typedef struct {
  uint8_t tp;
  uint16_t sz;
  const char *data;
} s16;

"""


class EncoderDecoder(object):

    def __init__( self ):
        self.ffi = cffi.FFI()
        self.ffi.cdef (_cdef)
        self.lib = self.ffi.dlopen(None)
        self._TYPE_STR = 99 
        self._TYPE_SZ = 1
        self._MAXLEN_TYPE = 1
        self._MAXLEN_STR = 2
        

    def enc_str( self, s ):
        sz = self._TYPE_SZ+self._MAXLEN_STR+len(s)
        cd = self.ffi.new('unsigned char *')
        bu = self.ffi.buffer(cd,sz)
        ct = self.ffi.new('uint8_t *',self._TYPE_STR)
        bt = self.ffi.buffer( ct,self._TYPE_SZ)
        
        bu[0] = bt[0] 
        clen = self.ffi.new( 'uint16_t*')
        clen[0] = len(s)
        clen_bu = self.ffi.buffer(clen,self._MAXLEN_STR)
         
        print "clen",clen[0] 
        bu[1] = clen_bu[0]
        bu[2] = clen_bu[1]
        ofs = 3
        for c in s: 
            bu[ofs] = c
            ofs+=1
        return cd

    def dec_str( self, cd ):
        meta_bu = self.ffi.buffer( cd,3) #!!! 
        clen = self.ffi.new( 'uint16_t*')
        tp = self.ffi.new( 'uint8_t*')
        tp_bu  = self.ffi.buffer( tp,self._TYPE_SZ)
        clen_bu = self.ffi.buffer(clen,self._MAXLEN_STR)
        
        tp_bu[0] = meta_bu[0]        
        clen_bu[0]=meta_bu[1]
        clen_bu[1]=meta_bu[2]

        data_bu = self.ffi.buffer( cd, 3 + clen[0])
        return (tp[0],clen[0]-1,data_bu[3:] )



