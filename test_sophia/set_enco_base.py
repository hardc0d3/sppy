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

print "set and encode from 1 to %d tuple keys and vals" % (count-1)
s = time.time()
for i in xrange(1,count):
    key = (i,i+1,i+2,i+3,i+4)
    val = "test string val %d" % i
     
    db.set_s_s( enco.encode(key),enco.encode(key) )
e = time.time()
es = e-s 
print "%f",es
print ""

print "close env",env.close()






