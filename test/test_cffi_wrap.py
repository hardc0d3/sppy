import sys
sys.path.append('../')
sys.path.append('../cfficodecs')

import _spapi_cdef
from _spapi_cffi import SpApiFFI
from _spapi_cffi import Wrap

sp_dl = '../build/sp.so'

sp = SpApiFFI( _spapi_cdef.cdef, sp_dl )

env = sp.env()

print "env:",env.cd

typ = sp.type(env)

print "typ env?",typ.decode()

ctl = sp.ctl(env)

typ = sp.type(ctl)

print "typ ctl?",typ.decode()

rc = sp.set( ctl, "sophia.path", "../test_data/" ) 

print "set ctl path", rc.decode()

rc = sp.set( ctl, "db", "spwrap" )

print "set ctl db name",rc

db = sp.get( ctl, "db.spwrap" )

print "db cd",db.cd

typ = sp.type(db)

# ._() == .decode()
print "typ db?",typ._()

rc = sp.open( env )

print "open env",rc._()

o = sp.object( db )

typ = sp.type(o)

print "is obj?",typ._()

key = "the_key"

value = "the_value"
szk = sp.ffi.cast("uint32_t",len(key))
szv = sp.ffi.cast("uint32_t",len(value))

rc = sp.set( o, "key",key,szk )

print "sp o set key", rc.decode()

rc = sp.set( o, "value",value,szv )

print "sp o set value" ,rc.decode()

rc = sp.set( db, o )

print "sp set db o",rc._()

rc = sp.destroy( o )

print "del o",rc._()

o = sp.object(db)

print "new o",o.cd

rc = sp.set( o, "key",key,szk )

print "sp o set key", rc.decode()
 
res_o = sp.get(db, o)

print "res obj",res_o.cd

sz = sp.ffi.new("uint32_t*")

res_v = sp.get(o,"value",sz )

#this is needed for save decode !!!
res_v.cd_sz = sz[0]
# !!!!

print "value: ", sz[0],res_v.decode()

sp.destroy(o)

sp.destroy(res_o)

rc = sp.destroy( env)

print "close env",rc._()

