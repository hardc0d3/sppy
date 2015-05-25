from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_cdef import sophia_api_cdef 
from sppy.spapi_cffi_codecs import *

dbname = 'test'
sp = SophiaApi( '../../sophia/libsophia.so.1.2.1',sophia_api_cdef )
codec_u32 = U32(sp.ffi)
keycount = 10

env = sp.env()
print "get env object",env.cd

typ = sp.type(env)
print "type env env?",typ.decode(0)

ctl = sp.ctl(env)
typ = sp.type(ctl)
print "type of ctl?",typ.decode(0)

rc = sp.set( ctl, "sophia.path", "../test_data/" )
print "set ctl path", rc.decode(0)


rc = sp.set( ctl, "db", dbname )
print "set ctl db name:%s"%dbname,rc


rc = sp.open( env )
print "open env",rc._(0)

db = sp.get( ctl, "db.%s"%dbname )
print "get ctl db.%s"%dbname,db.cd

typ = sp.type(db)
print "db type",typ._(0)

#rc = sp.open( db )
#print "open db",rc._(0)

for i in xrange(0,keycount):
    o = sp.object(db)

    key = codec_u32.encode( i ) 
    szk = sp.ffi.cast("uint32_t", 4 )
    szv = sp.ffi.new("uint32_t*")

    rc = sp.set( o, "key", key, szk)

    if rc._(0) != 0:
        print "err set query key"

    res = sp.get(db, o)

    if res.cd == sp.ffi.NULL:
        print "get err returned object is  NULL"
    else:
        val = sp.get( res, 'value', szv )
        print "decode value is size is %d "%szv[0], codec_u32.decode(val.cd,szv[0])
        # note U32 codecs know sz=4 uint32 and szv[0] is not used, but controlled
        sp.destroy(res) 

rc = sp.destroy(db)
print "destroy db",rc._(0)

rc = sp.destroy(env)
print "destroy env",rc._(0)




