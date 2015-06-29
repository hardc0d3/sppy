from sppy.spapi_cffi import SophiaApi, SophiaCmpApi
from sppy.spapi_cffi_codecs import *
from sppy.spapi_dict import SophiaDict
from sppy.spapi_cursor_dict import SophiaCursorDict
from sppy.spapi_cffi_cdef import sophia_api_cdefs

import cffi
import sp_index_cmp.cmpdef as cmpdef
from sppy.spapi_cffi_codecs import ListU32, U32
from random import randint

'''
ffi = cffi.FFI()
ffi.cdef ( cmpdef.cdef )
lib = ffi.dlopen("./sp_index_cmp/cmp.so")


compare_func = ffi.new("char[64]")
compare_arg = ffi.new("char[64]")
rc = lib.print_pointer( compare_func, ffi.cast("size_t",64) , lib.compare_u32list)
print "print pointer func",rc
rc = lib.print_pointer( compare_arg, ffi.cast("size_t",64) , ffi.new("size_t*",0 ) )
print "print pinter arg",rc
'''
# this wraps code above
cmpapi = SophiaCmpApi('./sp_index_cmp/cmp.so', cmpdef.cdef, 64, 'compare_u32list')
sp_path = '../test_data'
dbname = 'test_u32list'
sp = SophiaApi( '../lib/sophia/libsophia.so.1.2.2',sophia_api_cdefs['1.2.2'] )
keycodec = ListU32(sp.ffi)
valcodec = U32(sp.ffi)

dict_db_config = {
'sp.api':sp
,'key.codec':keycodec
,'value.codec':valcodec

}


env = sp.env()
print "get env object",env.cd

typ = sp.type(env)
print "type env env?",typ.decode(0)

ctl = sp.ctl(env)
typ = sp.type(ctl)
print "type of ctl?",typ.decode(0)

rc = sp.set( ctl, "sophia.path", sp_path )
print "set ctl path", rc.decode(0)


rc = sp.set( ctl, "db", dbname )
print "set ctl db name:%s"%dbname,rc

# attach custom comparsion
rc = sp.set( ctl, "db.%s.index.cmp"%dbname,  cmpapi.compare_func, cmpapi.compare_args)
print "set custom compare function",rc._(0)


rc = sp.open( env )
print "open env",rc._(0)

db = sp.get( ctl, "db.%s"%dbname )
print "get ctl db.%s"%dbname,db.cd


typ = sp.type(db)
print "db type",typ._(0)

dict_db =  SophiaDict(dict_db_config,db)

keycount = 15

keys = [
 [ 1000,100000,123412341]
,[ 435,1234,12341234   ]
,[ 1000,100000, 1234 ]
,[ 1000,1 ]
,[ 1000,1,1324]

]

for k in keys:
    dict_db[ k ]=10






c= SophiaCursorDict(dict_db)


def qry(query_list,ords): 
    global c
    c[query_list]=ords
    c.reset()

    for item in c:
        print item


qry([1000,],">=")
