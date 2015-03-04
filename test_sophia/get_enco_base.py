import sys
import time
sys.path.append('../')
sys.path.append('../cfficodecs')
import _spapi_cdef
from cfficodec import BaseCtoPy, BasePyCodec
from _spapi_cffi import SpApiFFI, Wrap
from sppy import Env, DB


sp_dl = '../build/sp.so'

spapi = SpApiFFI( sp_dl )




env  = Env( spapi, "/dataset/env_enco")
#print "env open",env.open()

db = DB( env, "sophia_base_test_enco")
codec = BaseCtoPy(env.sp)
enco = BasePyCodec(env.sp.ffi)
#print "db open",db.open()
print "env open",env.open()

u32 = codec.cast_uint32_t

count = 100000
"""
print "set from 1 to %d numerical keys" % (count-1)
s = time.time()
for i in xrange(1,count):
    db.set_u_s( i , "test number %d" % (i) )
e = time.time()
es = e - s
print "%f",es
print ""
"""

print "get and decode from 1 to %d tuple keys and vals" % (count-1)
s = time.time()
for i in xrange(1,count):
    key = (i,i+1,i+2,i+3,i+4)
    val = db._get_( enco, enco.encode(key) )
    #print val
    #print enco.decode(val)
e = time.time()
es = e-s 
print "t:",es
print ""

'''
sp = db.sp
db = db.db
o = sp.object(db)
cursor = sp.cursor(db,o)
if cursor.cd == sp.ffi.NULL:
    print "cursor.cd = NULL"
    exit()
while  o != sp.ffi.NULL:
    o = sp.get(cursor,o)
    sz = sp.ffi.new("uint32_t*")
    res_v = sp.get(o,"value",sz )
    print enco.decode( res_v.cd, sz[0])
'''

print "close env",env.close()






