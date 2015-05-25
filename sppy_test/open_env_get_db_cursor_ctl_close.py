from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_cdef import sophia_api_cdefs
from sppy.spapi_cffi_codecs import *

sp = SophiaApi( '../../sophia/sophia1.2.2/libsophia.so.1.2.2',sophia_api_cdefs['1.2.2'] )
codec_u32 = U32(sp.ffi)
dbname = 'test'


env = sp.env()
print "get env object",env.cd

typ = sp.type(env)
print "type env env?",typ.decode(0)

ctl = sp.ctl(env)

typ = sp.type(ctl)
print "type of ctl?",typ.decode(0)

rc = sp.set( ctl, "sophia.path", "../test_data/" )
print "set ctl path", rc._(0)

rc = sp.open( env )
print "open env",rc._(0)

rc = sp.set( ctl, "db", dbname )
print "set ctl db name:%s"%dbname,rc

db = sp.get( ctl, "db.%s"%dbname )
print "get ctl db.%s"%dbname,db.cd

cursor = sp.cursor(ctl)
print cursor.cd

o = sp.get(cursor)

szk = sp.ffi.new("uint32_t*")
szv = sp.ffi.new("uint32_t*")

while o.cd != sp.ffi.NULL:
    key = sp.get(o,"key",szk)
    val = sp.get(o,"value",szv)
    print key._(szk[0]),val._(szv[0])
    o = sp.get(cursor)

#print o.cd


rc = sp.destroy(env)
print "destroy env",rc



