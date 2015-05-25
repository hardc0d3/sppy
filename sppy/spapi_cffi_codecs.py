""" cffi based codecs c <-> py """


class AnsiString(object):
    def __init__(self, ffi ):
        self.ffi = ffi

    def encode(self,string):
        return self.ffi.new('char[]',string)

    def decode(self,cdata,sz):
        cstr =  self.ffi.new('char[%d]' % sz)
        cdata_buff = self.ffi.buffer(cdata,sz)
        cstr_buff  = self.ffi.buffer(cstr,sz)
        for i in xrange(sz):
            cstr_buff[i] = cdata_buff[i]
        return self.ffi.string(cstr)


class U32(object):
    def __init__(self, ffi ):
        self.ffi = ffi

    def encode(self,u32):
        cd = self.ffi.new('char[4]')
        cu32 = self.ffi.new('uint32_t*',u32)
        cd_buff = self.ffi.buffer(cd,4)
        u32_buff = self.ffi.buffer(cu32,4)
        cd_buff[0] = u32_buff[0]
        cd_buff[1] = u32_buff[1]
        cd_buff[2] = u32_buff[2]
        cd_buff[3] = u32_buff[3]
        return cd

    def decode(self,void_pointer,sz):
        cd = self.ffi.cast('char[4]',void_pointer)
        cu32 = self.ffi.new('uint32_t*')
        cd_buff = self.ffi.buffer(cd,4)
        u32_buff = self.ffi.buffer(cu32,4)
        u32_buff[0] = cd_buff[0]
        u32_buff[1] = cd_buff[1]
        u32_buff[2] = cd_buff[2]
        u32_buff[3] = cd_buff[3]
        return cu32[0]




class ListU32(object):
    def __init__(self, ffi ):
        self.ffi = ffi

    def encode(self, l):
        count = len(l)
        blen = (count+1)*4
        ccount  = self.ffi.new('uint32_t *',count )
        data = self.ffi.new('char[]',blen )
        count_buff = self.ffi.buffer(ccount,4)
        data_buff = self.ffi.buffer(data,blen) 
        for i in xrange(4):
           data_buff[i] = count_buff[i]
        pos = 0
        for j in xrange(count):
           cval = self.ffi.new('uint32_t *',l[j])
           val_buff = self.ffi.buffer(cval,4) 
           pos +=4 
           data_buff[pos] =   val_buff[0]
           data_buff[pos+1] = val_buff[1] 
           data_buff[pos+2] = val_buff[2]
           data_buff[pos+3] = val_buff[3]
        return data

    def decode(self, void_pointer, sz):
        ccount  = self.ffi.new('uint32_t *', 0 )
        count_buff = self.ffi.buffer(ccount,4)
        cdata = self.ffi.cast('char*',void_pointer )
        cdata_buff = self.ffi.buffer(cdata,sz) 
        for i in xrange(4):
           count_buff[i] = cdata_buff[i]

        blen = ((ccount[0] +1) * 4)
        assert blen == sz
        ll = list([None]*ccount[0])

        pos = 0
        for j in xrange(ccount[0]):
           cval = self.ffi.new('uint32_t *',0)
           val_buff = self.ffi.buffer(cval,4)  
           pos +=4 
           val_buff[0] = cdata_buff[pos]
           val_buff[1] = cdata_buff[pos+1]
           val_buff[2] = cdata_buff[pos+2]
           val_buff[3] = cdata_buff[pos+3]
           ll[j] = cval[0]
        return ll




