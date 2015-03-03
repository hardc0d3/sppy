import sys
import time
sys.path.append('../')
sys.path.append('../cfficodecs')
import _spapi_cdef
from cfficodec import BaseCtoPy
from _spapi_cffi import SpApiFFI
from _spapi_cffi import Wrap
from sppy import Env
from sppy import DB


sp_dl = '../build/sp.so'

spapi = SpApiFFI( sp_dl )




env  = Env( spapi, "/dataset/env1")
#print "env open",env.open()

db = DB( env, "sophia_base_test")
codec = BaseCtoPy(env.sp)

#print "db open",db.open()
print "env open",env.open()

u32 = codec.cast_uint32_t

count = 100000

print "get from 1 to %d numerical keys" % (count-1)
s = time.time()
for i in xrange(1,count):
    db.get_u( i )
e = time.time()
es = e - s 
print "%f",es
print ""


print "get from 1 to %d string keys" % (count-1)
s = time.time()
for i in xrange(1,count):
    key = "%d" % (i)
    db.get_s( key )
e = time.time()
es = e -s
print "%f",es
print ""



print "close env",env.close()






