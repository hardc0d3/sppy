class SophiaCtlDict(object):
    """sophia ctl object dict ctl_dict['ctl.key']='ctl.value'"""

    def __init__(self,sp,ctl):
        self.sp = sp
        self.ctl = ctl
        self.cnt = 0 
        if self.ctl == self.sp.ffi.NULL:
            raise Exception('ctl object is null')

    def __setitem__(self,key,value):
        """ set ctl key -> val"""
        rc = self.sp.set(self.ctl, key, value  )
        # check
        if rc._(0) != 0:
            raise KeyError('unable to set key val in controll interface')

    def __getitem__(self,key):
        """ get key -> value """
        ret_o = self.sp.get(self.ctl, key )
        if ret_o.cd == self.sp.ffi.NULL:
             raise KeyError('unable to get config object from ctl interface')
        sz = self.sp.ffi.new("uint32_t*")
        type_str = self.sp.type(ret_o)._(0)
        if type_str == 'database':
            return ret_o
        if type_str == 'object':
            ret_val = self.sp.get(ret_o,"value",sz )
            return ret_val._(sz[0])
        raise Exception("unhandled object type")

    def __iter__(self):
        """ iter ctl keys """
        if self.ctl == self.sp.ffi.NULL:
             raise Exception('ctl is null')
        cursor = self.sp.cursor(self.ctl)
        if cursor == self.sp.ffi.NULL:
            raise Exception('unable to get cursor: null')
        szk = self.sp.ffi.new('uint32_t*')
        o = self.sp.get(cursor)
        while o.cd != self.sp.ffi.NULL:
            ckey = self.sp.get(o,'key',szk)
            #cval = self.sp.get(self.o,'value',szv)
            self.cnt +=1
            o = self.sp.get(cursor)
            yield ckey._(szk[0])

    def iteritems(self):
        """ iter ctl keys and values """
        if self.ctl == self.sp.ffi.NULL:
             raise Exception('ctl is null')
        cursor = self.sp.cursor(self.ctl)
        if cursor == self.sp.ffi.NULL:
            raise Exception('unable to get cursor: null')
        szk = self.sp.ffi.new('uint32_t*')
        szv = self.sp.ffi.new('uint32_t*')
        o = self.sp.get(cursor)
        while o.cd != self.sp.ffi.NULL:
            ckey = self.sp.get(o,'key',szk)
            cval = self.sp.get(o,'value',szv)
            self.cnt +=1
            o = self.sp.get(cursor)
            yield ( ckey._(szk[0]), cval._(szv[0]) )

 
