#__getitem__(), __setitem__(), __delitem__(), and keys().


class SophiaDict(object):

    def __init__(self,cfg,db):
        self.cfg = cfg
        self.db = db 
        self.sp = cfg['sp.api']
        self.key_codec = cfg['key.codec']
        self.val_codec = cfg['value.codec']
        if self.db == self.sp.ffi.NULL:
            raise Exception('db object is null')

    def _setkey(self,key):
        """ set key only """
        ckey = self.key_codec.encode(key)
        o = self.sp.object(self.db)
        szk = self.sp.ffi.cast("uint32_t", self.sp.ffi.sizeof(ckey) )
        rc = self.sp.set(o, "key", ckey, szk )
        if rc._(0) != 0:
            raise KeyError('unable to set key field in object')
        rcd = self.sp.set(self.db, o)
        if rcd._(0) != 0:
            raise KeyError('unable to set key only object in db')
        #return rcd._(0)


    def _setkeyval(self,key,val):
        """ set key -> val"""
        ckey = self.key_codec.encode(key)
        cval = self.val_codec.encode(val)
        #sp = self.sp
        #db = self.db
        o = self.sp.object(self.db)
        szk = self.sp.ffi.cast('uint32_t', self.sp.ffi.sizeof(ckey) )
        szv = self.sp.ffi.cast('uint32_t', self.sp.ffi.sizeof(cval) )
        rc = self.sp.set(o, 'key', ckey, szk )
        rc = self.sp.set(o, 'value',cval, szv )
        # check
        if rc._(0) != 0:
            raise KeyError('unable to set key val fields in object')
        rcd = self.sp.set(self.db, o)
        if rcd._(0) != 0:
            raise KeyError('unable to set key and value object in db')
        #return rcd._(0)

    def __getitem__(self,key):
        """ get key -> value """
        ckey = self.key_codec.encode(key)
        o = self.sp.object(self.db)
        szk = self.sp.ffi.cast("uint32_t", self.sp.ffi.sizeof(ckey) )
        rc = self.sp.set(o, "key", ckey, szk )
        if rc._(0) != 0:
            raise KeyError('unable to set key field in object')
        ret_o = self.sp.get(self.db, o)
        if ret_o.cd == self.sp.ffi.NULL:
             raise KeyError('unable to get key object from db')
        sz = self.sp.ffi.new("uint32_t*")
        ret_val = self.sp.get(ret_o,"value",sz )
        ret_dec = self.val_codec.decode(ret_val.cd,sz[0])
        rc = self.sp.destroy(ret_o)
        if rc._(0) != 0:
            raise KeyError('unable to destroy return object')
        return ret_dec

    def __setitem__(self,key,value):
       """ set key->val or key only"""
       if value == None:
           self._setkey(key)
       self._setkeyval(key,value)

    def __delitem__(self,key):
        """ del item by key """
        ckey = self.key_codec.encode(key)
        o = self.sp.object(self.db)
        szk = self.sp.ffi.cast("uint32_t", self.sp.ffi.sizeof(ckey) )
        rc = self.sp.set(o, "key", ckey, szk )

        if rc._(0) != 0:
            raise KeyError('unbale to set key field in object')

        rc = self.sp.delete(self.db,o)
        if rc._(0) !=0:
            rcd = self.sp.destroy(o)
            if rcd._(0) != 0:
                raise KeyError('unable to del key and destroy obj')
            raise KeyError('unable to del key')

        rcd = self.sp.destroy(o)
        if rcd._(0) != 0:
            raise KeyError('unable to destroy obj after del')
        #return rc.cd[0]


        
