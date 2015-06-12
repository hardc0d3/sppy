from sppy.spapi_cffi import SophiaApi
from sppy.spapi_cffi_cdef import sophia_api_cdefs
from sppy.spapi_cffi_codecs import *
from random import randint

sp = SophiaApi( '/hardcode/devenv/rivadb/sophia_was/libsophia.so.1.2.1',sophia_api_cdefs['1.2.2'] )
codec_u32 = U32(sp.ffi)
dbname = 'test_low_api'


env = sp.env()
print "get env object",env.cd

typ = sp.type(env)
print "type env env?",typ.decode(0)

ctl = sp.ctl(env)

typ = sp.type(ctl)
print "type of ctl?",typ.decode(0)

rc = sp.set( ctl, "sophia.path", "../test_data/low1" )
print "set ctl path", rc._(0)

rc = sp.set( ctl, "db", dbname )
print "set ctl db name:%s"%dbname,rc

db = sp.get( ctl, "db.%s"%dbname )
print "get ctl db.%s"%dbname,db.cd

rc = sp.open( env )
print "open env",rc._(0)



keycount=40
l=[0]*keycount

for i in xrange(0,keycount):
    l[i]=randint(1000,2000)

import list_data
l = list_data.l
l=list(set(l))
keycount = len(l)
print l

int_type="uint32_t"

itp = int_type+"*"
for i in xrange(0,keycount):
    o = sp.object(db)
    key = sp.ffi.new(itp,l[i])
    szk = sp.ffi.cast("uint32_t",sp.ffi.sizeof(key) )
    rc = sp.set( o, "key",key,szk )
    if rc._(0) == 0:
        rc = sp.set(db, o)
    else:
        print "err in set key in o"
    if rc._(0) != 0:
        print "err in set key in db"
    #rc = sp.destroy( o )
print "OK"

resl=[]

o = sp.object(db)
itp =int_type +"*"
ikey = sp.ffi.new(itp,1500)
szk = sp.ffi.cast("uint32_t",sp.ffi.sizeof(ikey) )

sp.set(o,"order",">=")
sp.set(o,"key", ikey, szk )
cursor = sp.cursor(db, o)
typ = sp.type(cursor)
print "cursor?",typ._(0)
sz = sp.ffi.new("uint32_t*")

o = sp.get( cursor, o )
while o.cd != sp.ffi.NULL:
    key = sp.get(o,"key",sz)
    ckey = sp.ffi.cast(itp,key.cd)
    #print ckey[0]
    resl.append(ckey[0])
    o = sp.get( cursor, o )


print resl

