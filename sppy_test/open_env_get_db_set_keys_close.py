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
    value = codec_u32.encode(i+1000)

    szk = sp.ffi.cast("uint32_t", 4 )
    szv = sp.ffi.cast("uint32_t", 4 )

    rc = sp.set( o, "key", key, szk)
    rc = sp.set( o, "value", value, szv)

    if rc._(0) == 0:
        rc = sp.set(db, o)
        print "set %d->%d"%(i,i+1000),rc._(0)
        rc = sp.destroy(o)
        print "del o",rc._(0)
    else:
        print "err in set key,val in o"
    if rc._(0) != 0:
        print "err in set key in db"


rc = sp.destroy(db)
print "destroy db",rc._(0)

rc = sp.destroy(env)
print "destroy env",rc._(0)




