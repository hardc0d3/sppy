import sys
sys.path.append('../')
sys.path.append('../cfficodecs')

import _spapi_cdef
from _spapi_cffi import SpApiFFI
from _spapi_cffi import Wrap

sp_dl = '../build/sp.so'

sp = SpApiFFI( sp_dl )

env = sp.env()

print "env:",env.cd

typ = sp.type(env)

print "typ env?",typ.decode(0)

ctl = sp.ctl(env)

typ = sp.type(ctl)

print "typ ctl?",typ.decode(0)

rc = sp.set( ctl, "sophia.path", "../test_data/" ) 

print "set ctl path", rc.decode(0)

rc = sp.set( ctl, "db", "spwrap" )

print "set ctl db name",rc

db = sp.get( ctl, "db.spwrap" )

print "db cd",db.cd

typ = sp.type(db)

# ._() == .decode()
print "typ db?",typ._(0)

rc = sp.open( env )

print "open env",rc._(0)

o = sp.object( db )

typ = sp.type(o)

print "is obj?",typ._(0)

#key = "the_key"
key = sp.ffi.new("int*",10000)
print key[0]
value = "the_value"
#value = sp.ffi.cast("int",34)

#szk = sp.ffi.cast("uint32_t",len(key))
szv = sp.ffi.cast("uint32_t",len(value))
print "sz key",sp.ffi.sizeof(key)

szk = sp.ffi.cast("uint32_t",sp.ffi.sizeof(key) )
#szv = sp.ffi.cast("uint32_t",sp.ffi.sizeof(value) )
print szk,szv

rc = sp.set( o, "key",key,szk )

print "sp o set key", rc.decode(0)

rc = sp.set( o, "value",value,szv )

#rc = sp.lib.sp_set( o.cd, 

print "sp o set value" ,rc.decode(0)

rc = sp.set( db, o )

#rc = sp.lib.sp_set( db.cd, o.cd )

print "db set"
print "sp set db o",rc._(0)

rc = sp.destroy( o )

print "del o",rc._(0)

o = sp.object(db)

print "new o",o.cd

rc = sp.set( o, "key",key,szk )

print "sp o set key", rc.decode(0)
 
res_o = sp.get(db, o)

print "res obj",res_o.cd

sz = sp.ffi.new("uint32_t*")

res_v = sp.get(o,"value",sz )

print "value: ", res_v.decode(sz[0])


sp.destroy(o)

sp.destroy(res_o)

rc = sp.destroy( env)

print "close env",rc._(0)

