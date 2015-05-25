#__getitem__(), __setitem__(), __delitem__(), and keys().

class CurrentStep(object):
    def __init__(self,iterator):
        self.it = iterator
        self.cnt = 0
        self.curr = None
        
        self.curr = self.it.next()
        # will raise StopIteration if there is not at least one item 
        #self.cnt +=1

    def step(self):
        self.curr = self.it.next()
        self.cnt +=1

    def current(self):
        return self.curr
            

class SophiaCursorDict(object):

    def __init__(self,db_dict):
        self.db = db_dict.db 
        self.sp = db_dict.sp 
        self.key_codec = db_dict.key_codec 
        self.val_codec = db_dict.val_codec 
        self.cnt = 0
        if self.db == self.sp.ffi.NULL:
            raise Exception('db object is null')
        self.cursor = self.sp.ffi.NULL
        self.query_o = self.sp.ffi.NULL
        self.o = self.sp.ffi.NULL
        self.order = None
        self.key =  None
        self.current_key = None
        self.current_val = None

    def __setitem__(self,key,order):
        """ set cursor search key in order | order could be some of that strings: > < <= >= """
        ckey = self.key_codec.encode(key)
        self.query_o = self.sp.object(self.db)
        szk = self.sp.ffi.cast('uint32_t', self.sp.ffi.sizeof(ckey) )
        rc = self.sp.set(self.query_o, 'key', ckey, szk )
        if rc._(0) != 0:
            raise  KeyError('unable to set key field for cursor object')
        rc = self.sp.set(self.query_o, 'order',order )
        if rc._(0) != 0:
            raise  KeyError('unable to set order field for cursor object')

        self.cursor = self.sp.cursor(self.db, self.query_o)
        self.order = order
        self.key = key 
        #if self.cursor = self.sp.ffi.NULL:
        #    raise KeyError('unable to get cursor is null')

    def reset(self):
        self.__setitem__(self.key,self.order)
       

    def __iter__(self):
        """ iter keys """
        if self.cursor == self.sp.ffi.NULL:
            raise Exception('cursor is null')
        sz = self.sp.ffi.new('uint32_t*')
        self.o = self.sp.get(self.cursor,self.query_o)
        while self.o.cd != self.sp.ffi.NULL:
            ckey = self.sp.get(self.o,'key',sz)
            key = self.key_codec.decode(ckey.cd,sz[0])
            self.cnt +=1
            self.o = self.sp.get(self.cursor, self.query_o)
            yield key 

    def iteritems(self):
        """ iter keys and values """
        if self.cursor == self.sp.ffi.NULL:
            raise Exception('cursor is null')

        szk = self.sp.ffi.new('uint32_t*')
        szv = self.sp.ffi.new('uint32_t*')
        self.o = self.sp.get(self.cursor,self.query_o)
        while self.o.cd != self.sp.ffi.NULL:
            ckey = self.sp.get(self.o,'key',szk)
            cval = self.sp.get(self.o,'value',szv)
            key = self.key_codec.decode(ckey.cd,szk[0])
            val =  self.val_codec.decode(cval.cd,szv[0])
            self.cnt +=1
            self.o = self.sp.get(self.cursor, self.query_o)
            yield (key,val)




