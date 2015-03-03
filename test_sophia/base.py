import sys
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




env  = Env( spapi, "../test_data/env1")
#print "env open",env.open()

db = DB( env, "sophia_base_test")
codec = BaseCtoPy(env.sp)

#print "db open",db.open()
print "env open",env.open()

u32 = codec.cast_uint32_t

count = 10000

print "set from 1 to %d numerical keys"

for i in xrange(1,count):
    db.set_u_s( i , "test number %d" % i )


print "close db", db.close()
print "close env",env.close()






